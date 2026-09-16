# Progress

Checklist of the work done in this repository. Newest on top.

## 2026-09-16
- [x] **Find extra points across masters** (`paths/find_extra_points_across_masters.py`)
      — LCS node diff against the leanest master, ARROW annotations on the
      extra nodes, plus path count / start point / direction / component /
      anchor diagnostics. Covered by `tests/test_find_extra_points.py`.

## Backlog
- [ ] `components/check_corner_components_across_masters.py` tags its annotations
      via `GSAnnotation.userData`, which does not exist — the cleanup on re-run
      never removes anything. Port it to the `.text` marker used by
      `find_extra_points_across_masters.py`.
