from __future__ import print_function
# MenuTitle: Plus sign bounding box
# -*- coding: utf-8 -*-

__doc__="""

This script creates guidelines that cover the same space as the plus signs bounding box. Useful when designing math symbols.

"""

font = Glyphs.font
glyphs = font.glyphs

current_layer = font.selectedLayers[0]
ref_glyph = font.glyphs['plus'].layers[font.selectedLayers[0].layerId]

w = ref_glyph.bounds.size.width
h = ref_glyph.bounds.size.height
xo = ref_glyph.bounds.origin.x
yo = ref_glyph.bounds.origin.y

g1_x = xo
g1_y = yo
g1_ang = 0

g1 = [g1_x, g1_y, g1_ang]

g2_x = g1_x
g2_y = g1_y + h
g2_ang = 90

g2 = [g2_x, g2_y, g2_ang]

g3_x = g2_x + w
g3_y = g2_y
g3_ang = 0

g3 = [g3_x, g3_y, g3_ang]

g4_x = g3_x
g4_y = g1_y
g4_ang = 90

g4 = [g4_x, g4_y, g4_ang]

g5 = [xo, yo+h/2, 0] 

# list of points
lp = g1, g2, g3, g4, g5

# those lines above was copied from mekkablue's script "Remove Local Guides in Selected Glyphs"
# comment it if you do not want to del local guidelines before create the guide box.
for thisLayer in Glyphs.font.selectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo()
	thisLayer.guideLines = None
	thisGlyph.endUndo()
	print("  %s" % thisGlyph.name)

for p in lp:
	newGuide = GSGuideLine()
	newGuide.position = NSPoint(p[0], p[1])
	newGuide.angle = p[2]
	current_layer.guides.append(newGuide)
