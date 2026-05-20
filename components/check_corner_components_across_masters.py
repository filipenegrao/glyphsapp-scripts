# MenuTitle: Check Corner Components Across Masters
# -*- coding: utf-8 -*-
"""
Checks whether the corner components of the selected glyph(s)
are consistent in number across all masters.

— Detailed report in the Macro Window
— Opens a tab with glyphs that have discrepancies
— Marks nodes with annotations where inconsistencies are found:
    CIRCLE  → position of the corner in the reference master
    ARROW   → missing corner in this master (approximate position)
    TEXT    → summary of missing corners
"""

# ---------------------------------------------------------------
#  Tag to identify annotations created by this script
#  (allows automatic cleanup on re-runs)
# ---------------------------------------------------------------
ANNOTATION_TAG = "com.analogico.cornerCheck"

font = Glyphs.font

if not font:
    print("No font open.")
else:
    Glyphs.clearLog()
    Glyphs.showMacroWindow()

    selected_glyphs = [layer.parent for layer in font.selectedLayers]
    seen = set()
    unique_glyphs = []
    for g in selected_glyphs:
        if g.name not in seen:
            seen.add(g.name)
            unique_glyphs.append(g)

    if not unique_glyphs:
        print("No glyph selected.")
    else:
        masters = font.masters
        total_issues = 0
        total_checked = 0
        glyphs_with_issues = []

        print("=" * 60)
        print("  CORNER COMPONENTS — CHECK ACROSS MASTERS")
        print("=" * 60)
        print("  Font: %s" % font.familyName)
        print("  Masters: %s" % ", ".join(m.name for m in masters))
        print("  Glyphs to check: %d" % len(unique_glyphs))
        print("=" * 60)
        print()

        # -------------------------------------------------------
        #  Clear annotations from previous runs
        # -------------------------------------------------------
        for glyph in unique_glyphs:
            for master in masters:
                layer = glyph.layers[master.id]
                if layer is None:
                    continue
                to_remove = []
                for i, ann in enumerate(layer.annotations):
                    try:
                        if ann.userData and ann.userData.get(ANNOTATION_TAG):
                            to_remove.append(i)
                    except:
                        pass
                for i in reversed(to_remove):
                    del layer.annotations[i]

        # -------------------------------------------------------
        #  Helper: collect corner info from a layer
        # -------------------------------------------------------
        def get_corner_info(layer):
            """
            Returns a list of dicts:
              { 'name': str, 'position': NSPoint or None }
            """
            corners = []
            for hint in layer.hints:
                if hint.type == CORNER:
                    name = hint.name if hint.name else "(unnamed)"
                    pos = None
                    if hint.originNode:
                        pos = NSPoint(hint.originNode.position.x,
                                      hint.originNode.position.y)
                    corners.append({
                        "name": name,
                        "position": pos,
                    })
            return corners

        # -------------------------------------------------------
        #  Analysis
        # -------------------------------------------------------
        for glyph in unique_glyphs:
            total_checked += 1

            master_data = {}
            for master in masters:
                layer = glyph.layers[master.id]
                if layer is None:
                    master_data[master.id] = {
                        "name": master.name, "corners": [], "layer": None
                    }
                    continue
                master_data[master.id] = {
                    "name": master.name,
                    "corners": get_corner_info(layer),
                    "layer": layer,
                }

            # Count by name
            all_names = set()
            name_counts = {}
            for mid, data in master_data.items():
                nc = {}
                for c in data["corners"]:
                    nc[c["name"]] = nc.get(c["name"], 0) + 1
                    all_names.add(c["name"])
                name_counts[mid] = nc

            # Detect discrepancy
            has_issue = False
            total_per_master = {
                mid: len(data["corners"])
                for mid, data in master_data.items()
            }
            if len(set(total_per_master.values())) > 1:
                has_issue = True

            for cn in all_names:
                per_master = set()
                for mid in master_data:
                    per_master.add(name_counts[mid].get(cn, 0))
                if len(per_master) > 1:
                    has_issue = True

            if not has_issue:
                if all_names:
                    names_str = ", ".join(
                        "%s x%d" % (cn, list(name_counts.values())[0].get(cn, 0))
                        for cn in sorted(all_names)
                    )
                    print("[ok]  %s  (%s)" % (glyph.name, names_str))
                continue

            # --- Discrepancy found ---
            total_issues += 1
            glyphs_with_issues.append(glyph)

            print("[!!]  %s" % glyph.name)

            # Reference master = the one with the most corners
            ref_mid = max(master_data,
                          key=lambda mid: len(master_data[mid]["corners"]))
            ref_name_counts = name_counts[ref_mid]

            for mid, data in master_data.items():
                layer = data["layer"]
                n_corners = len(data["corners"])
                ref_count = len(master_data[ref_mid]["corners"])
                tag = "[ok]" if n_corners == ref_count else "[!!]"
                print("    %s %s: %d corners" % (tag, data["name"], n_corners))

                if layer is None:
                    continue

                # Detail discrepancy by name
                for cn in sorted(all_names):
                    expected = ref_name_counts.get(cn, 0)
                    actual = name_counts[mid].get(cn, 0)
                    if actual != expected:
                        print("       > %s: has %d, expected %d" % (
                            cn, actual, expected))

                # ----- VISUAL ANNOTATIONS -----

                # 1) In the REFERENCE master: mark each corner with CIRCLE
                if mid == ref_mid:
                    for c in data["corners"]:
                        if c["position"]:
                            ann = GSAnnotation()
                            ann.type = CIRCLE
                            ann.position = NSPoint(
                                c["position"].x, c["position"].y)
                            ann.width = 30
                            try:
                                ann.userData = {ANNOTATION_TAG: True}
                            except:
                                pass
                            layer.annotations.append(ann)

                # 2) Masters with FEWER corners: mark where they are missing
                if n_corners < ref_count:
                    # Text annotation with summary
                    missing_lines = []
                    for cn in sorted(all_names):
                        expected = ref_name_counts.get(cn, 0)
                        actual = name_counts[mid].get(cn, 0)
                        if actual < expected:
                            missing_lines.append(
                                "%s (missing %d)" % (cn, expected - actual))

                    if missing_lines:
                        ann = GSAnnotation()
                        ann.type = TEXT
                        ann.text = "MISSING CORNERS:\n%s" % "\n".join(missing_lines)
                        ann.position = NSPoint(0, -100)
                        ann.width = 300
                        try:
                            ann.userData = {ANNOTATION_TAG: True}
                        except:
                            pass
                        layer.annotations.append(ann)

                    # Arrows at approximate positions of missing corners
                    # Uses positions from the reference master as a guide
                    ref_corners = master_data[ref_mid]["corners"]
                    own_tracker = {}
                    for c in data["corners"]:
                        own_tracker[c["name"]] = own_tracker.get(
                            c["name"], 0) + 1

                    for rc in ref_corners:
                        rn = rc["name"]
                        have = own_tracker.get(rn, 0)
                        need = ref_name_counts.get(rn, 0)
                        if have < need and rc["position"]:
                            ann = GSAnnotation()
                            ann.type = ARROW
                            ann.position = NSPoint(
                                rc["position"].x, rc["position"].y)
                            ann.width = 40
                            try:
                                ann.userData = {ANNOTATION_TAG: True}
                            except:
                                pass
                            layer.annotations.append(ann)
                            own_tracker[rn] = have + 1

            print()

        # -------------------------------------------------------
        #  Open tab
        # -------------------------------------------------------
        if glyphs_with_issues:
            tab_text = "/" + "/".join(g.name for g in glyphs_with_issues)
            font.newTab(tab_text)
            print("Tab opened with %d glyph(s)." % len(glyphs_with_issues))

        # -------------------------------------------------------
        #  Final summary
        # -------------------------------------------------------
        print()
        print("-" * 60)
        if total_issues == 0:
            print("All good! %d glyph(s) checked, no discrepancies found." % total_checked)
        else:
            print("%d glyph(s) with discrepancies out of %d checked." % (
                total_issues, total_checked))
            print()
            print("VISUAL LEGEND (annotations):")
            print("  CIRCLE  = corner position in the reference master")
            print("  ARROW   = missing corner in this master (approx. position)")
            print("  TEXT    = summary of missing corners")
            print()
            print("Re-run the script to clear previous annotations.")
        print("-" * 60)
