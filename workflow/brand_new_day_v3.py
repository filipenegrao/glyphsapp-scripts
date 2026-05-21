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

try:
    from fonttools.ttLib import TTFont
    from fonttools.pens.boundsPen import BoundsPen
    from fonttools.pens.recordingPen import RecordingPen
    _FONTTOOLS_AVAILABLE = True
except ImportError:
    _FONTTOOLS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Pure utilities
# ---------------------------------------------------------------------------

def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def strip_date_from_name(family_name: str) -> str:
    """Remove trailing YYYY-MM-DD date from a font family name."""
    return re.sub(r'\s*\d{4}-\d{2}-\d{2}$', '', family_name).strip()


def copy_snapshot(source: Path, dest: Path) -> None:
    """Copy source folder to dest. No-op if dest already exists."""
    if dest.exists():
        return
    shutil.copytree(source, dest)


def _glyph_stats(ttfont: Any, glyph_name: str) -> dict[str, Any] | None:
    """Return point count and bounding box for a glyph, or None if glyph not in font."""
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
    except Exception:  # corrupt or unreadable font file
        return None

    diff: dict[str, Any] = {}
    try:
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
    finally:
        prev_font.close()
        curr_font.close()

    return diff or None


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
        return'<p class="nd">No OTF diff for this session.</p>';
      const rows=Object.entries(diff).map(([n,d])=>{{
        const pc=dc(d.points_before,d.points_after);
        const bw_prev=d.bbox_before?d.bbox_before[2]-d.bbox_before[0]:null;
        const bw_curr=d.bbox_after?d.bbox_after[2]-d.bbox_after[0]:null;
        return`<tr><td>${{n}}</td>
          <td>${{d.points_before??'—'}}→${{d.points_after??'—'}}
            <span class="${{pc}}">(${{ds(d.points_before,d.points_after)}})</span></td>
          <td class="${{dc(bw_prev,bw_curr)}}">${{ds(bw_prev,bw_curr)}}</td></tr>`;
      }}).join('');
      return`<table><thead><tr><th>Glyph</th><th>Points</th><th>Width Δ</th></tr></thead>
        <tbody>${{rows}}</tbody></table>`;
    }}
    function render(){{
      if(!DATA.length){{document.body.innerHTML+='<p style="color:#444;margin-top:2rem">No sessions yet.</p>';return}}
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
    font_path      = Path(font.filepath)
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

    # 3. Collect changed glyphs
    last_modified_date = datetime.fromtimestamp(
        os.path.getmtime(str(new_font_path))
    ).date()
    changed_glyphs = _get_changed_glyphs(font, last_modified_date)

    # 4. Git snapshot
    try:
        git_commit_snapshot(root, new_font_path, len(changed_glyphs), today)
    except Exception as e:
        print(f"[brand_new_day_v3] git step skipped: {e}")

    # 5. Prepare folders and find previous OTF for diff
    otf_folder.mkdir(exist_ok=True)
    logs_folder.mkdir(exist_ok=True)

    existing_otfs = sorted(otf_folder.glob("*.otf"), key=lambda p: p.stat().st_mtime, reverse=True)
    prev_otf = existing_otfs[0] if existing_otfs else None

    # 6. Generate OTFs
    for instance in font.instances:
        instance.generate(FontPath=str(otf_folder))

    # 7. Diff new vs previous OTF
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

    # 10. Notify
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
