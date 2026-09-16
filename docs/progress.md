# Progress

Checklist of the work done in this repository. Newest on top.

## 2026-09-16
- [x] **Find extra points across masters** (`paths/find_extra_points_across_masters.py`)
      — LCS node diff against the leanest master, ARROW annotations on the
      extra nodes, plus path count / start point / direction / component /
      anchor diagnostics. Rotation-aware alignment, so a path that also
      starts at a different node does not get innocent nodes blamed.
      Covered by `tests/test_find_extra_points.py` (22 tests).
- [ ] Run it inside Glyphs on a font with a known extra node — the pure diff
      is tested, the Glyphs side (annotations, cleanup, scope) is not.

## Backlog
- [ ] `components/check_corner_components_across_masters.py` tags its annotations
      via `GSAnnotation.userData`, which does not exist — the cleanup on re-run
      never removes anything. Port it to the `.text` marker used by
      `find_extra_points_across_masters.py`.
