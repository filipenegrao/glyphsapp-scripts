# Brand New Day v3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `workflow/brand_new_day_with_log_v2.py` with a v3 script that snapshots the font folder, commits to git, generates OTFs, diffs them with fonttools, and writes a self-contained HTML dashboard from a JSON log.

**Architecture:** Pure utility functions (path math, log management, HTML generation, OTF diffing) are isolated at the top of the script so they are importable and testable without Glyphs running. Glyphs-dependent calls (font access, OTF generation, notifications) live in `main()`, which is called only when `Glyphs` is available in the runtime namespace. Data flows one-way: Glyphs → JSON log → HTML dashboard.

**Tech Stack:** Python 3.10+ (Glyphs 3 bundled), `pathlib`, `shutil`, `subprocess`, `json`, `datetime`, `fonttools` (optional, graceful fallback)

---

## File Structure

| File | Action | Responsibility |
|---|---|---|
| `workflow/brand_new_day_v3.py` | Create | Main script: all pure functions + `main()` |
| `tests/test_brand_new_day_v3.py` | Create | Tests for all pure functions |

---

### Task 1: Script skeleton + pure path utilities

**Files:**
- Create: `workflow/brand_new_day_v3.py`
- Create: `tests/test_brand_new_day_v3.py`

- [ ] **Step 1: Write failing tests for `strip_date_from_name` and `today_str`**

Create `tests/test_brand_new_day_v3.py`:

```python
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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd /path/to/glyphsapp-scripts
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: `ModuleNotFoundError: No module named 'brand_new_day_v3'`

- [ ] **Step 3: Create `workflow/brand_new_day_v3.py` with the skeleton**

```python
# MenuTitle: Brand New Day v3
# -*- coding: utf-8 -*-
"""
Daily font snapshot with git history, OTF diff, and HTML dashboard.

Pure functions live at module level (importable, testable without Glyphs).
Glyphs-specific code is isolated in main(), called only inside Glyphs.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Pure utilities
# ---------------------------------------------------------------------------

def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def strip_date_from_name(family_name: str) -> str:
    """Remove trailing YYYY-MM-DD date from a font family name."""
    return re.sub(r'\s*\d{4}-\d{2}-\d{2}$', '', family_name).strip()
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add workflow/brand_new_day_v3.py tests/test_brand_new_day_v3.py
git commit -m "feat: scaffold brand_new_day_v3 with path utilities and tests"
```

---

### Task 2: Snapshot logic

**Files:**
- Modify: `workflow/brand_new_day_v3.py`
- Modify: `tests/test_brand_new_day_v3.py`

- [ ] **Step 1: Write failing test for `copy_snapshot`**

Append to `tests/test_brand_new_day_v3.py`:

```python
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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
python -m pytest tests/test_brand_new_day_v3.py::test_copy_snapshot_creates_dest -v
```

Expected: `AttributeError: module 'brand_new_day_v3' has no attribute 'copy_snapshot'`

- [ ] **Step 3: Implement `copy_snapshot`**

Add to `workflow/brand_new_day_v3.py` after `strip_date_from_name`:

```python
def copy_snapshot(source: Path, dest: Path) -> None:
    """Copy source folder to dest. No-op if dest already exists."""
    if dest.exists():
        return
    shutil.copytree(source, dest)
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add workflow/brand_new_day_v3.py tests/test_brand_new_day_v3.py
git commit -m "feat: add copy_snapshot with idempotency"
```

---

### Task 3: Git integration

**Files:**
- Modify: `workflow/brand_new_day_v3.py`
- Modify: `tests/test_brand_new_day_v3.py`

- [ ] **Step 1: Write failing tests for `git_commit_snapshot`**

Append to `tests/test_brand_new_day_v3.py`:

```python
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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
python -m pytest tests/test_brand_new_day_v3.py::test_git_commit_snapshot_inits_and_commits -v
```

Expected: `AttributeError: module 'brand_new_day_v3' has no attribute 'git_commit_snapshot'`

- [ ] **Step 3: Implement `git_commit_snapshot`**

Add to `workflow/brand_new_day_v3.py`:

```python
_GITIGNORE_CONTENT = """-OTFs/
-logs/
*.pyc
"""


def git_commit_snapshot(
    root: Path,
    glyphs_file: Path,
    n_changed: int,
    today: str,
) -> None:
    """Init git repo at root if needed, then commit the .glyphs file."""
    git = ["git", "-C", str(root)]

    def run(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [*git, *args],
            capture_output=True,
            text=True,
        )

    if not (root / ".git").exists():
        run("init")
        run("config", "user.email", "glyphs-script@local")
        run("config", "user.name", "Brand New Day")
        gitignore = root / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(_GITIGNORE_CONTENT)
        run("add", ".gitignore")
        run("commit", "-m", "chore: init font project repo")

    rel = glyphs_file.relative_to(root)
    run("add", str(rel))

    status = run("status", "--porcelain")
    if not status.stdout.strip():
        return  # nothing staged

    msg = f"font: {today} snapshot — {n_changed} glyph{'s' if n_changed != 1 else ''} modified"
    run("commit", "-m", msg)
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 8 tests PASS

- [ ] **Step 5: Commit**

```bash
git add workflow/brand_new_day_v3.py tests/test_brand_new_day_v3.py
git commit -m "feat: add git_commit_snapshot with auto-init"
```

---

### Task 4: OTF diff with fonttools

**Files:**
- Modify: `workflow/brand_new_day_v3.py`
- Modify: `tests/test_brand_new_day_v3.py`

- [ ] **Step 1: Write failing tests for `get_glyph_stats` and `compute_otf_diff`**

Append to `tests/test_brand_new_day_v3.py`:

```python
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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
python -m pytest tests/test_brand_new_day_v3.py::test_compute_otf_diff_returns_none_without_fonttools -v
```

Expected: `AttributeError: module 'brand_new_day_v3' has no attribute '_FONTTOOLS_AVAILABLE'`

- [ ] **Step 3: Implement `compute_otf_diff`**

Add to `workflow/brand_new_day_v3.py` (after imports block, before `today_str`):

```python
try:
    from fonttools.ttLib import TTFont
    from fonttools.pens.boundsPen import BoundsPen
    from fonttools.pens.recordingPen import RecordingPen
    _FONTTOOLS_AVAILABLE = True
except ImportError:
    _FONTTOOLS_AVAILABLE = False
```

Then add the functions:

```python
def _glyph_stats(ttfont: Any, glyph_name: str) -> dict[str, Any] | None:
    """Return point count and bounding box for a glyph. Requires fonttools."""
    glyph_set = ttfont.getGlyphSet()
    if glyph_name not in glyph_set:
        return None
    rec = RecordingPen()
    bp = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(rec)
    glyph_set[glyph_name].draw(bp)
    points = sum(
        len(args)
        for op, args in rec.value
        if op in ("moveTo", "lineTo", "curveTo", "qCurveTo")
    )
    return {
        "points": points,
        "bbox": list(bp.bounds) if bp.bounds else None,
    }


def compute_otf_diff(
    prev_otf: Path,
    curr_otf: Path,
    changed_glyphs: list[str],
) -> dict[str, Any] | None:
    """
    Compare glyph outlines between two OTF files.
    Returns None if fonttools is unavailable or either file is missing.
    """
    if not _FONTTOOLS_AVAILABLE:
        return None
    if not prev_otf.exists() or not curr_otf.exists():
        return None
    try:
        prev_font = TTFont(str(prev_otf))
        curr_font = TTFont(str(curr_otf))
    except Exception:
        return None

    diff: dict[str, Any] = {}
    for name in changed_glyphs:
        prev_stats = _glyph_stats(prev_font, name)
        curr_stats = _glyph_stats(curr_font, name)
        if prev_stats is None and curr_stats is None:
            continue
        diff[name] = {
            "points_before": prev_stats["points"] if prev_stats else None,
            "points_after":  curr_stats["points"]  if curr_stats  else None,
            "bbox_before":   prev_stats["bbox"]    if prev_stats else None,
            "bbox_after":    curr_stats["bbox"]    if curr_stats  else None,
        }
    return diff or None
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 10 tests PASS

- [ ] **Step 5: Commit**

```bash
git add workflow/brand_new_day_v3.py tests/test_brand_new_day_v3.py
git commit -m "feat: add compute_otf_diff with fonttools, graceful fallback"
```

---

### Task 5: JSON log management

**Files:**
- Modify: `workflow/brand_new_day_v3.py`
- Modify: `tests/test_brand_new_day_v3.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_brand_new_day_v3.py`:

```python
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
```

- [ ] **Step 2: Run to confirm they fail**

```bash
python -m pytest tests/test_brand_new_day_v3.py::test_load_log_returns_empty_list_when_missing -v
```

Expected: `AttributeError: module 'brand_new_day_v3' has no attribute 'load_log'`

- [ ] **Step 3: Implement the three log functions**

Add to `workflow/brand_new_day_v3.py`:

```python
def load_log(log_path: Path) -> list[dict]:
    """Read log.json; return [] if missing. Back up and reset if corrupt."""
    if not log_path.exists():
        return []
    try:
        return json.loads(log_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        log_path.rename(log_path.with_suffix(".json.bak"))
        return []


def upsert_log_entry(entries: list[dict], new_entry: dict) -> list[dict]:
    """Replace existing entry for the same date, or append if new."""
    for i, e in enumerate(entries):
        if e.get("date") == new_entry["date"]:
            entries[i] = new_entry
            return entries
    entries.append(new_entry)
    return entries


def save_log(log_path: Path, entries: list[dict]) -> None:
    log_path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
```

- [ ] **Step 4: Run all tests**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 16 tests PASS

- [ ] **Step 5: Commit**

```bash
git add workflow/brand_new_day_v3.py tests/test_brand_new_day_v3.py
git commit -m "feat: add JSON log management (load, upsert, save)"
```

---

### Task 6: HTML dashboard generation

**Files:**
- Modify: `workflow/brand_new_day_v3.py`
- Modify: `tests/test_brand_new_day_v3.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_brand_new_day_v3.py`:

```python
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
```

- [ ] **Step 2: Run to confirm they fail**

```bash
python -m pytest tests/test_brand_new_day_v3.py::test_generate_dashboard_html_returns_string -v
```

Expected: `AttributeError: module 'brand_new_day_v3' has no attribute 'generate_dashboard_html'`

- [ ] **Step 3: Implement `generate_dashboard_html`**

Add to `workflow/brand_new_day_v3.py`:

```python
_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Type Design Dashboard</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',monospace;
          background:#0d0d0d;color:#e0e0e0;padding:2rem}}
    h1{{font-size:1.5rem;font-weight:600;margin-bottom:.25rem}}
    .sub{{color:#888;font-size:.85rem;margin-bottom:2rem}}
    .session{{border:1px solid #222;border-radius:6px;margin-bottom:1rem;overflow:hidden}}
    .sh{{display:flex;align-items:center;gap:1rem;padding:.75rem 1rem;
         cursor:pointer;background:#161616}}
    .sh:hover{{background:#1e1e1e}}
    .dot{{width:12px;height:12px;border-radius:50%;flex-shrink:0}}
    .sdate{{font-weight:600;font-size:.9rem}}
    .scount{{color:#888;font-size:.8rem;margin-left:auto}}
    .sb{{padding:1rem;display:none;border-top:1px solid #222}}
    .sb.open{{display:block}}
    .gl{{display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:1rem}}
    .gt{{background:#222;border-radius:3px;padding:.2rem .5rem;
         font-size:.78rem;font-family:monospace}}
    table{{width:100%;border-collapse:collapse;font-size:.82rem}}
    th{{text-align:left;color:#666;font-weight:500;padding:.4rem .5rem;
        border-bottom:1px solid #222}}
    td{{padding:.4rem .5rem;border-bottom:1px solid #111;font-family:monospace}}
    .up{{color:#4ade80}}.down{{color:#f87171}}.same{{color:#666}}
    .nd{{color:#444;font-style:italic;font-size:.82rem}}
  </style>
</head>
<body>
  <h1 id="fn"></h1>
  <div class="sub" id="sub"></div>
  <div id="sessions"></div>
  <script>
    const DATA={data_json};
    function dotColor(n){{return n===0?'#333':n<5?'#3b82f6':n<20?'#8b5cf6':'#f59e0b'}}
    function dc(a,b){{return a===null||b===null?'same':a<b?'up':a>b?'down':'same'}}
    function ds(a,b){{
      if(a===null||b===null)return'—';
      const d=b-a;return d===0?'\xb10':(d>0?'+':'')+d
    }}
    function renderDiff(diff){{
      if(!diff||!Object.keys(diff).length)
        return '<p class="nd">No OTF diff for this session.</p>';
      const rows=Object.entries(diff).map(([n,d])=>{{
        const pc=dc(d.points_before,d.points_after);
        const bw_prev=d.bbox_before?d.bbox_before[2]-d.bbox_before[0]:null;
        const bw_curr=d.bbox_after?d.bbox_after[2]-d.bbox_after[0]:null;
        return`<tr><td>${{n}}</td>
          <td>${{d.points_before??'—'}}→${{d.points_after??'—'}}
            <span class="${{pc}}">($ {{ds(d.points_before,d.points_after)}})</span></td>
          <td class="${{dc(bw_prev,bw_curr)}}">${{ds(bw_prev,bw_curr)}}</td></tr>`;
      }}).join('');
      return`<table><thead><tr><th>Glyph</th><th>Points</th><th>Width Δ</th></tr></thead>
        <tbody>${{rows}}</tbody></table>`;
    }}
    function render(){{
      if(!DATA.length){{document.body.innerHTML+='<p>No sessions yet.</p>';return}}
      const latest=DATA[DATA.length-1];
      document.getElementById('fn').textContent=latest.font_name;
      document.getElementById('sub').textContent=
        `Last updated: ${{latest.date}} \xb7 ${{DATA.length}} session${{DATA.length!==1?'s':''}}`;
      const c=document.getElementById('sessions');
      [...DATA].reverse().forEach((s,i)=>{{
        const n=s.glyphs_changed_count||0,id='s'+i;
        const div=document.createElement('div');
        div.className='session';
        div.innerHTML=`
          <div class="sh" onclick="toggle('${{id}}')">
            <div class="dot" style="background:${{dotColor(n)}}"></div>
            <span class="sdate">${{s.date}}</span>
            <span class="scount">${{n}} glyph${{n!==1?'s':''}} changed</span>
          </div>
          <div class="sb" id="${{id}}">
            <div class="gl">${{(s.glyphs_changed||[]).map(g=>`<span class="gt">${{g}}</span>`).join('')}}</div>
            ${{renderDiff(s.otf_diff)}}
          </div>`;
        c.appendChild(div);
      }});
    }}
    function toggle(id){{document.getElementById(id).classList.toggle('open')}}
    render();
  </script>
</body>
</html>"""


def generate_dashboard_html(entries: list[dict]) -> str:
    data_json = json.dumps(entries, ensure_ascii=False)
    return _HTML_TEMPLATE.format(data_json=data_json)
```

- [ ] **Step 4: Run all tests**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 19 tests PASS

- [ ] **Step 5: Commit**

```bash
git add workflow/brand_new_day_v3.py tests/test_brand_new_day_v3.py
git commit -m "feat: add HTML dashboard generator with embedded JSON"
```

---

### Task 7: OTF pre-scan helper

**Files:**
- Modify: `workflow/brand_new_day_v3.py`
- Modify: `tests/test_brand_new_day_v3.py`

This task adds `find_previous_otf(otf_folder, current_otf_path)` — finds the most recently modified OTF in `-OTFs/` *before* the current build so the diff knows what to compare against.

- [ ] **Step 1: Write failing test**

Append to `tests/test_brand_new_day_v3.py`:

```python
import time

def test_find_previous_otf_returns_none_when_folder_empty(tmp_path):
    assert bnd.find_previous_otf(tmp_path, tmp_path / "curr.otf") is None

def test_find_previous_otf_returns_older_file(tmp_path):
    old = tmp_path / "MyFont-Regular-old.otf"
    old.write_text("old")
    time.sleep(0.05)
    curr = tmp_path / "MyFont-Regular.otf"
    curr.write_text("new")
    # curr is the "just generated" file — previous should be old
    result = bnd.find_previous_otf(tmp_path, curr)
    assert result == old
```

- [ ] **Step 2: Run to confirm they fail**

```bash
python -m pytest tests/test_brand_new_day_v3.py::test_find_previous_otf_returns_none_when_folder_empty -v
```

Expected: `AttributeError: module 'brand_new_day_v3' has no attribute 'find_previous_otf'`

- [ ] **Step 3: Implement `find_previous_otf`**

Add to `workflow/brand_new_day_v3.py`:

```python
def find_previous_otf(otf_folder: Path, current_otf: Path) -> Path | None:
    """
    Return the most recently modified OTF in otf_folder that is not current_otf.
    Returns None if none found.
    """
    candidates = [
        p for p in otf_folder.glob("*.otf")
        if p.resolve() != current_otf.resolve()
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)
```

- [ ] **Step 4: Run all tests**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 21 tests PASS

- [ ] **Step 5: Commit**

```bash
git add workflow/brand_new_day_v3.py tests/test_brand_new_day_v3.py
git commit -m "feat: add find_previous_otf for diff baseline lookup"
```

---

### Task 8: Main execution block (Glyphs wiring)

**Files:**
- Modify: `workflow/brand_new_day_v3.py`

This task adds `main()` which uses the Glyphs API. It cannot be unit tested without Glyphs running — verify manually by running the script inside Glyphs.

- [ ] **Step 1: Add `main()` to `workflow/brand_new_day_v3.py`**

Append at the bottom of the file:

```python
# ---------------------------------------------------------------------------
# Glyphs-dependent execution
# ---------------------------------------------------------------------------

def _get_changed_glyphs(font: Any, reference_date: Any) -> list[str]:
    """Return names of glyphs whose lastChange matches reference_date."""
    changed = []
    for glyph in font.glyphs:
        if glyph.lastChange is not None:
            if glyph.lastChange.date() == reference_date:
                changed.append(glyph.name)
    return changed


def main() -> None:
    font = Glyphs.font  # type: ignore[name-defined]

    if font is None or font.filepath is None:
        Glyphs.showNotification(  # type: ignore[name-defined]
            "Brand New Day v3",
            "No font open or font has not been saved yet.",
        )
        return

    today = today_str()
    font_path     = Path(font.filepath)
    current_folder = font_path.parent
    root           = current_folder.parent
    new_folder     = root / today
    new_font_path  = new_folder / font_path.name
    otf_folder     = root / "-OTFs"
    logs_folder    = root / "-logs"
    log_json_path  = logs_folder / "log.json"
    dashboard_path = logs_folder / "dashboard.html"

    # 1. Snapshot
    copy_snapshot(current_folder, new_folder)

    # 2. Rename font, save, close, open new
    base_name = strip_date_from_name(font.familyName)
    font.familyName = f"{base_name} {today}"
    font.save()
    font.close()
    Glyphs.open(str(new_font_path))  # type: ignore[name-defined]
    font = Glyphs.font  # type: ignore[name-defined]

    # 3. Collect changed glyphs (from the now-open new font)
    last_modified_date = datetime.fromtimestamp(
        os.path.getmtime(str(new_font_path))
    ).date()
    changed_glyphs = _get_changed_glyphs(font, last_modified_date)

    # 4. Git snapshot
    try:
        git_commit_snapshot(root, new_font_path, len(changed_glyphs), today)
    except Exception as e:
        print(f"[brand_new_day_v3] git step skipped: {e}")

    # 5. Pre-scan existing OTFs for diff baseline
    otf_folder.mkdir(exist_ok=True)
    logs_folder.mkdir(exist_ok=True)

    # Find a representative OTF for diff (first instance, same stem as family)
    existing_otfs = sorted(otf_folder.glob("*.otf"), key=lambda p: p.stat().st_mtime, reverse=True)
    prev_otf = existing_otfs[0] if existing_otfs else None

    # 6. Generate OTFs
    for instance in font.instances:
        instance.generate(FontPath=str(otf_folder))

    # 7. Find the newly generated OTF for diff (most recent after generation)
    new_otfs = sorted(otf_folder.glob("*.otf"), key=lambda p: p.stat().st_mtime, reverse=True)
    curr_otf = new_otfs[0] if new_otfs else None

    otf_diff = None
    if prev_otf and curr_otf:
        otf_diff = compute_otf_diff(prev_otf, curr_otf, changed_glyphs)

    # 8. Append to log.json
    entries = load_log(log_json_path)
    new_entry = {
        "date":                 today,
        "font_name":            font.familyName,
        "font_path":            str(new_font_path),
        "glyphs_changed":       changed_glyphs,
        "glyphs_changed_count": len(changed_glyphs),
        "otf_diff":             otf_diff,
    }
    entries = upsert_log_entry(entries, new_entry)
    save_log(log_json_path, entries)

    # 9. Regenerate dashboard.html
    dashboard_path.write_text(
        generate_dashboard_html(entries),
        encoding="utf-8",
    )

    # 10. Notify + open macro window
    Glyphs.showNotification(  # type: ignore[name-defined]
        "Brand New Day v3",
        f"Snapshot ready: {new_folder.name} · {len(changed_glyphs)} glyphs changed",
    )
    Glyphs.showMacroWindow()  # type: ignore[name-defined]

    print("*" * 52)
    print(f"Have a nice day!")
    print(f"New folder:  {new_folder}")
    print(f"New font:    {new_font_path}")
    print(f"Dashboard:   {dashboard_path}")
    print(f"Glyphs changed today ({len(changed_glyphs)}): {', '.join(changed_glyphs) or 'none'}")
    print(f"OTF diff:    {'yes' if otf_diff else 'no'}")
    print("*" * 52)


# Run when executed inside Glyphs
try:
    Glyphs  # type: ignore[name-defined]
    main()
except NameError:
    pass  # running outside Glyphs (e.g. during tests) — do nothing
```

- [ ] **Step 2: Run all existing tests to confirm nothing broke**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 21 tests PASS

- [ ] **Step 3: Manual smoke test inside Glyphs**

    1. Open any `.glyphs` file in Glyphs 3
    2. Make a small edit to a glyph (so `lastChange` is today)
    3. Run the script via Scripts menu → Brand New Day v3
    4. Verify:
       - A new dated folder was created one level up from the font
       - The font was closed and the new copy opened
       - `-OTFs/` folder exists and contains at least one `.otf`
       - `-logs/log.json` exists and contains one entry with today's date
       - `-logs/dashboard.html` exists and opens in a browser showing the session

- [ ] **Step 4: Commit**

```bash
git add workflow/brand_new_day_v3.py
git commit -m "feat: add main() Glyphs execution block — completes brand_new_day_v3"
```

---

### Task 9: Cleanup and menu title

**Files:**
- Modify: `workflow/brand_new_day_v3.py`

- [ ] **Step 1: Verify the menu title comment is at line 1**

The first line of `workflow/brand_new_day_v3.py` must be:

```python
# MenuTitle: Brand New Day v3
```

Glyphs reads this to show the script in the Scripts menu. Confirm it is present.

- [ ] **Step 2: Run full test suite one final time**

```bash
python -m pytest tests/test_brand_new_day_v3.py -v
```

Expected: all 21 tests PASS, 0 failures.

- [ ] **Step 3: Final commit**

```bash
git add workflow/brand_new_day_v3.py
git commit -m "chore: verify MenuTitle and finalize brand_new_day_v3"
```

---

## Self-Review Checklist

- [x] **Spec: snapshot** → Task 2 (`copy_snapshot`)
- [x] **Spec: font rename** → Task 8 (`strip_date_from_name` + `main()`)
- [x] **Spec: git init + commit** → Task 3 (`git_commit_snapshot`)
- [x] **Spec: OTF generation** → Task 8 (`main()` step 6)
- [x] **Spec: fonttools diff** → Task 4 (`compute_otf_diff`) + Task 7 (`find_previous_otf`)
- [x] **Spec: log.json append with upsert** → Task 5 (`load_log`, `upsert_log_entry`, `save_log`)
- [x] **Spec: HTML dashboard regeneration** → Task 6 (`generate_dashboard_html`)
- [x] **Spec: `distutils` removal** → Task 2 uses `shutil.copytree`
- [x] **Spec: `pathlib` throughout** → all functions use `Path`
- [x] **Spec: graceful fallback (fonttools, git)** → `_FONTTOOLS_AVAILABLE` guard + try/except in `main()`
- [x] **Spec: corrupt log.json recovery** → `load_log` backs up + resets
- [x] **Spec: idempotent (same day re-run)** → `copy_snapshot` no-op if dest exists; `upsert_log_entry` updates existing date
- [x] **Types consistent across tasks:** `Path` used everywhere; `list[str]` for `changed_glyphs`; `dict[str, Any] | None` for `otf_diff`
- [x] **No placeholders or TBDs found**
