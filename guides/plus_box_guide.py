# MenuTitle: Plus sign bounding box
# -*- coding: utf-8 -*-

__doc__ = """
Creates guidelines matching the bounding box of the plus glyph.
Useful when designing math symbols.
"""

font = Glyphs.font
current_layer = font.selectedLayers[0]
ref_glyph = font.glyphs['plus'].layers[current_layer.layerId]

w = ref_glyph.bounds.size.width
h = ref_glyph.bounds.size.height
xo = ref_glyph.bounds.origin.x
yo = ref_glyph.bounds.origin.y

guide_params = [
    (xo,      yo,        0),
    (xo,      yo + h,    90),
    (xo + w,  yo + h,    0),
    (xo + w,  yo,        90),
    (xo,      yo + h/2,  0),
]

for thisLayer in Glyphs.font.selectedLayers:
    thisGlyph = thisLayer.parent
    thisGlyph.beginUndo()
    thisLayer.guides = []
    for x, y, ang in guide_params:
        newGuide = GSGuide()
        newGuide.position = x, y
        newGuide.angle = ang
        thisLayer.guides.append(newGuide)
    thisGlyph.endUndo()
    print("  %s" % thisGlyph.name)
