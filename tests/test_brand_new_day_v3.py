import json
import os
import re
import shutil as _shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'workflow'))

# Stub Glyphs so module imports without crashing outside Glyphs
import types
glyphs_stub = types.ModuleType('Glyphs')
sys.modules.setdefault('Glyphs', glyphs_stub)

import brand_new_day_v3 as bnd


def test_strip_date_removes_trailing_date():
    assert bnd.strip_date_from_name("MyFont 2026-05-20") == "MyFont"

def test_strip_date_leaves_undated_name():
    assert bnd.strip_date_from_name("MyFont") == "MyFont"

def test_strip_date_handles_multiple_words():
    assert bnd.strip_date_from_name("My Font Display 2025-01-01") == "My Font Display"

def test_today_str_format():
    assert re.match(r'\d{4}-\d{2}-\d{2}', bnd.today_str())

def test_copy_snapshot_creates_dest(tmp_path):
    src = tmp_path / "2026-05-19"
    src.mkdir()
    (src / "MyFont.glyphs").write_text("dummy")
    dest = tmp_path / "2026-05-20"
    bnd.copy_snapshot(src, dest)
    assert (dest / "MyFont.glyphs").exists()

def test_copy_snapshot_is_idempotent(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "f.glyphs").write_text("x")
    dest = tmp_path / "dest"
    bnd.copy_snapshot(src, dest)
    bnd.copy_snapshot(src, dest)  # second call must not raise
    assert (dest / "f.glyphs").exists()


def test_git_commit_snapshot_inits_and_commits(tmp_path):
    repo = tmp_path / "font-project"
    repo.mkdir()
    dated = repo / "2026-05-20"
    dated.mkdir()
    glyphs_file = dated / "MyFont.glyphs"
    glyphs_file.write_text("glyphs data")

    bnd.git_commit_snapshot(repo, glyphs_file, n_changed=3, today="2026-05-20")

    result = subprocess.run(
        ["git", "-C", str(repo), "log", "--oneline"],
        capture_output=True, text=True
    )
    assert "2026-05-20 snapshot" in result.stdout

def test_git_commit_snapshot_skips_when_nothing_staged(tmp_path):
    repo = tmp_path / "font-project"
    repo.mkdir()
    dated = repo / "2026-05-20"
    dated.mkdir()
    glyphs_file = dated / "MyFont.glyphs"
    glyphs_file.write_text("glyphs data")

    # First commit
    bnd.git_commit_snapshot(repo, glyphs_file, n_changed=3, today="2026-05-20")
    # Second call same file, same content — should not raise
    bnd.git_commit_snapshot(repo, glyphs_file, n_changed=3, today="2026-05-20")


def test_compute_otf_diff_returns_none_without_fonttools(monkeypatch):
    monkeypatch.setattr(bnd, '_FONTTOOLS_AVAILABLE', False)
    result = bnd.compute_otf_diff(Path("a.otf"), Path("b.otf"), ["a", "b"])
    assert result is None

def test_compute_otf_diff_returns_none_when_file_missing():
    result = bnd.compute_otf_diff(
        Path("/nonexistent/prev.otf"),
        Path("/nonexistent/curr.otf"),
        ["a"],
    )
    assert result is None


def test_load_log_returns_empty_list_when_missing(tmp_path):
    assert bnd.load_log(tmp_path / "log.json") == []

def test_load_log_returns_entries(tmp_path):
    log = tmp_path / "log.json"
    log.write_text(json.dumps([{"date": "2026-05-19"}]))
    assert bnd.load_log(log) == [{"date": "2026-05-19"}]

def test_load_log_backs_up_corrupt_file(tmp_path):
    log = tmp_path / "log.json"
    log.write_text("NOT JSON {{{{")
    result = bnd.load_log(log)
    assert result == []
    assert (tmp_path / "log.json.bak").exists()

def test_upsert_log_entry_adds_new(tmp_path):
    entries = [{"date": "2026-05-19", "font_name": "A"}]
    new = {"date": "2026-05-20", "font_name": "B", "glyphs_changed": [], "glyphs_changed_count": 0, "otf_diff": None}
    result = bnd.upsert_log_entry(entries, new)
    assert len(result) == 2

def test_upsert_log_entry_updates_existing(tmp_path):
    existing = {"date": "2026-05-20", "font_name": "A", "glyphs_changed": [], "glyphs_changed_count": 0, "otf_diff": None}
    updated  = {"date": "2026-05-20", "font_name": "B", "glyphs_changed": ["a"], "glyphs_changed_count": 1, "otf_diff": None}
    result = bnd.upsert_log_entry([existing], updated)
    assert len(result) == 1
    assert result[0]["font_name"] == "B"

def test_save_log_writes_valid_json(tmp_path):
    log = tmp_path / "log.json"
    bnd.save_log(log, [{"date": "2026-05-20"}])
    assert json.loads(log.read_text()) == [{"date": "2026-05-20"}]

def test_generate_dashboard_html_returns_string():
    entries = [{"date": "2026-05-20", "font_name": "MyFont 2026-05-20",
                "glyphs_changed": ["a", "b"], "glyphs_changed_count": 2, "otf_diff": None}]
    html = bnd.generate_dashboard_html(entries)
    assert isinstance(html, str)
    assert "<!DOCTYPE html>" in html

def test_generate_dashboard_html_embeds_data():
    entries = [{"date": "2026-05-20", "font_name": "MyFont",
                "glyphs_changed": ["ampersand"], "glyphs_changed_count": 1, "otf_diff": None}]
    html = bnd.generate_dashboard_html(entries)
    assert "ampersand" in html

def test_generate_dashboard_html_handles_empty_entries():
    html = bnd.generate_dashboard_html([])
    assert "<!DOCTYPE html>" in html

