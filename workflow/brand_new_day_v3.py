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
