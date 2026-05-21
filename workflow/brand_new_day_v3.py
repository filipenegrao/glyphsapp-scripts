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


def copy_snapshot(source: Path, dest: Path) -> None:
    """Copy source folder to dest. No-op if dest already exists."""
    if dest.exists():
        return
    shutil.copytree(source, dest)


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
