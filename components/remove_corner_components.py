# MenuTitle: Remove Corner Components
# -*- coding: utf-8 -*-
"""
Removes all corner components from all masters
of the selected glyph(s).

— Detailed report in the Macro Window
"""

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
        total_removed = 0

        print("=" * 60)
        print("  REMOVE CORNER COMPONENTS")
        print("=" * 60)
        print("  Font: %s" % font.familyName)
        print("  Masters: %s" % ", ".join(m.name for m in masters))
        print("  Glyphs: %d" % len(unique_glyphs))
        print("=" * 60)
        print()

        for glyph in unique_glyphs:
            glyph_removed = 0

            for master in masters:
                layer = glyph.layers[master.id]
                if layer is None:
                    continue

                corners = [h for h in layer.hints if h.type == CORNER]
                for hint in corners:
                    layer.hints.remove(hint)

                if corners:
                    print("  %s / %s: removed %d corner(s)" % (
                        glyph.name, master.name, len(corners)))
                    glyph_removed += len(corners)

            if glyph_removed == 0:
                print("  %s: no corner components found" % glyph.name)

            total_removed += glyph_removed

        print()
        print("-" * 60)
        print("Done. %d corner component(s) removed." % total_removed)
        print("-" * 60)
