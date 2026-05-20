# Brand New Day v3 — Design Spec

**Date:** 2026-05-20
**Script:** `workflow/brand_new_day_v3.py`
**Replaces:** `workflow/brand_new_day_with_log_v2.py`

---

## Goal

A single script that, on each working session:

1. Creates a fresh dated snapshot of the font project folder
2. Commits that snapshot to git for proper history
3. Generates OTF files and diffs them against the previous build
4. Appends structured session data to a JSON log
5. Regenerates a self-contained HTML dashboard showing the changelog and diffs

---

## Output Files

All outputs live under `{root}/` (one level above the current dated font folder):

| Path | Purpose |
|---|---|
| `{root}/{YYYY-MM-DD}/` | Dated copy of the font folder (snapshot) |
| `{root}/-OTFs/` | Generated OTF files from each run |
| `{root}/-logs/log.json` | Structured session log (appended each run) |
| `{root}/-logs/dashboard.html` | Self-contained visual dashboard (regenerated each run) |
| `{root}/.git/` | Git repo tracking the font file history |

---

## Script Flow

### 1. Snapshot

- Detect `CURRENT_FOLDER` from the open font's `filepath`
- Compute `NEW_FOLDER_PATH = {root}/{TODAY}`
- If it doesn't exist: copy via `shutil.copytree(CURRENT_FOLDER, NEW_FOLDER_PATH)`
- If it already exists: skip copy (idempotent — safe to run twice in a day)

### 2. Rename Font

- Strip any trailing `YYYY-MM-DD` from `familyName`
- Append today's date: `"{BaseName} {TODAY}"`
- Assign back to `FONT.familyName`

### 3. Save, Close, Open New

- `FONT.save()` then `FONT.close()`
- `Glyphs.open(NEW_FILE_PATH)`

### 4. Git Snapshot

- Check for `{root}/.git`; if absent, run `git init {root}`
- Create `{root}/.gitignore` if absent, ignoring `-OTFs/` and `-logs/` (binary/generated)
- `git -C {root} add {YYYY-MM-DD}/{GLYPHS_FILENAME}`
- `git -C {root} commit -m "font: {TODAY} snapshot — {N} glyphs modified"`
- If nothing staged (no changes detected by git), skip commit silently

### 5. Generate OTFs

- Create `{root}/-OTFs/` if absent
- For each instance in `Glyphs.font.instances`: `instance.generate(FontPath=OTF_FOLDER)`

### 6. Fonttools Diff

- Find the most recent OTF in `-OTFs/` that predates today's build (by filename or mtime)
- If found and `fonttools` is importable:
  - Load both OTFs with `fonttools.ttLib.TTFont`
  - For each glyph in the `glyf` or `CFF ` table, extract point count and bounding box
  - Compute delta: `{glyphName: {points_before, points_after, bbox_before, bbox_after}}`
- If no previous OTF or fonttools unavailable: store `otf_diff: null`

### 7. Append to `log.json`

Each run appends one object to the top-level JSON array:

```json
{
  "date": "2026-05-20",
  "font_name": "MyFont 2026-05-20",
  "font_path": "/path/to/2026-05-20/MyFont.glyphs",
  "glyphs_changed": ["a", "b", "ampersand"],
  "glyphs_changed_count": 3,
  "otf_diff": {
    "a": {
      "points_before": 24,
      "points_after": 26,
      "bbox_before": [20, -10, 480, 700],
      "bbox_after": [22, -10, 478, 702]
    }
  }
}
```

- Read existing `log.json` if present; append new entry; write back
- If the same date already exists in the log, update that entry (idempotent)

### 8. Regenerate `dashboard.html`

Python writes a single `.html` file that:

- Embeds the full `log.json` content as a JS variable inside a `<script>` tag
- Uses vanilla JS to render the UI (no CDN, no dependencies, works offline)
- Layout:
  - **Header** — font family name + last run date
  - **Timeline** — one row per session, dot sized/colored by `glyphs_changed_count`
  - **Session detail** (click to expand) — list of `glyphs_changed`
  - **OTF diff table** (within expanded session) — glyph | points Δ | bbox Δ, colored green/red
  - **Empty state** — shown when `glyphs_changed` is empty for a session

---

## Error Handling

| Situation | Behavior |
|---|---|
| Font not saved (no `filepath`) | Exit early with `Glyphs.showNotification` error |
| `{TODAY}` folder already exists | Skip copy, continue with rest of script |
| `fonttools` not installed | Log `otf_diff: null`, continue |
| No previous OTF to diff against | Log `otf_diff: null`, continue |
| Git not available on PATH | Skip git steps, log warning to Macro window |
| `log.json` corrupted | Back it up as `log.json.bak`, start fresh |

---

## Code Quality Changes vs v2

| v2 | v3 |
|---|---|
| `distutils.dir_util.copy_tree` (removed in Python 3.12) | `shutil.copytree` |
| `os.path` string concatenation everywhere | `pathlib.Path` throughout |
| `dict_to_md_tag` references `k` after for-loop (scope bug) | Rewritten as clean function |
| Writes `.md` and `.txt` log (both) | Writes `log.json` only; HTML replaces both |
| No git integration | `git init` + commit on each run |

---

## Dependencies

| Dependency | Required | Notes |
|---|---|---|
| `pathlib` | Yes | stdlib |
| `shutil` | Yes | stdlib |
| `subprocess` | Yes | stdlib (for git commands) |
| `json` | Yes | stdlib |
| `fonttools` | No | Graceful fallback if absent; install via `pip install fonttools` in Glyphs' Python env |

---

## Out of Scope

- No UI dialog / settings panel (keep zero-friction single-click execution)
- No cloud sync or remote backup
- No automatic opening of `dashboard.html` (user opens manually)
- No removal of old dated folders (user manages disk space)
