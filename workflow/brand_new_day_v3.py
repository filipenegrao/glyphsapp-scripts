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
