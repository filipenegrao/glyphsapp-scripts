# MenuTitle: Narrow Diacritics maker, step 1
# -*- coding: utf-8 -*-

__doc__ = """

This is the first step to create narrow diacrits for /i and /j. 
It duplicates "dieresiscomb", "gravecomb", "acutecomb", "brevecomb", "tildecomb", "macroncomb", "ogonekcomb" addind a ".narrow" suffix.
The next step will rename those glyphs to .narrow and update the components for /i and /j.

"""

font = Glyphs.font

diacritics = ["dieresiscomb", "gravecomb", "acutecomb", "brevecomb", "tildecomb", "macroncomb", "ogonekcomb"]
narrow_diacritics = []

# Duplicate glyph combs
for d in diacritics:
    g_narrow = "%s.narrow" % d
    narrow_diacritics.append(g_narrow)

    if font.glyphs[g_narrow]:
        print "%s already exist." % g_narrow
        pass

    else:
        g = font.glyphs[d]
        g.duplicate(g_narrow)
        print "%s was created" % g_narrow


for i, master in enumerate(font.masters):
    layer1 = font.glyphs['idotless'].layers[font.masters[i].id]

    for d in narrow_diacritics:
        layer2 = font.glyphs[d].layers[font.masters[i].id]
        background_layer2 = layer2.background
        background_layer2 = []

        for path in layer1.paths:
            new_path = path.copy()
            background_layer2.append(new_path)
            print "idotless %s was copy to %s %s background layer" % (layer1.name, d, layer2.name)

ndiacritics = '/'.join([i for i in narrow_diacritics])

glyph_str = ''

for g in narrow_diacritics:
    glyph_str += "/" + g

font.newTab(glyph_str)
Glyphs.showMacroWindow()

