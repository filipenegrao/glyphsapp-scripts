# Progress

Checklist of the work done in this repository. Newest on top.

## 2026-09-16
- [x] **Find extra points across masters** (`paths/find_extra_points_across_masters.py`)
      — LCS node diff against the leanest master, ARROW annotations on the
      extra nodes, plus path count / start point / direction / component /
      anchor diagnostics. Rotation-aware alignment, so a path that also
      starts at a different node does not get innocent nodes blamed.
      Covered by `tests/test_find_extra_points.py` (22 tests).
- [x] Fixed: the arrows pointed at the wrong nodes. The diff compared bare
      node types, and a rounded contour is periodic ("oocoocooc..."), so every
      minimal alignment tied and the backtrack picked an arbitrary one — right
      count, wrong place. Nodes now carry their corner/smooth flag and ties are
      settled by normalized position along the contour.
- [ ] Re-run inside Glyphs on the ExtraBold that reported 2 extra nodes and
      confirm both arrows land on the stems, not on the top-left corner.
- [ ] The Glyphs side (annotation placement, userData cleanup, scope) still has
      no coverage — only the alignment is tested.

## Backlog
- [ ] `components/check_corner_components_across_masters.py` tags its annotations
      via `GSAnnotation.userData`, which does not exist — the cleanup on re-run
      never removes anything. Port it to the `.text` marker used by
      `find_extra_points_across_masters.py`.
