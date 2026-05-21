import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'workflow'))

import importlib, types

# Stub out Glyphs so the module imports without crashing
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
    import re
    assert re.match(r'\d{4}-\d{2}-\d{2}', bnd.today_str())

import subprocess
import tempfile, shutil as _shutil

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
