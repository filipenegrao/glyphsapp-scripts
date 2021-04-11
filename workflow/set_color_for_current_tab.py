# MenuTitle: Set color for current tab
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """


"""


# Change this to define a different color
R, G, B, A = 247.0, 74.0, 62.9, 1

f = Glyphs.font

for layer in f.selectedLayers:
	glyph = layer.parent
	glyph.colorObject = (R, G, B, A)