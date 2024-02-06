#MenuTitle: Copy glyph's foregrounds to backgrounds.
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from __future__ import print_function

__doc__="""

Copy Master's foregrounds to its respective backgrounds.
Just a quick way to do a copy, when you need to modify all the masters of a glyph.
** Warning: ** this script erases the background layer's paths that wore previously there.
Comment the following line to avoid that: bg_layer.paths = []

"""

import copy
import traceback


font = Glyphs.font
glyphs = font.glyphs

# get active layer
layer = font.selectedLayers[0]

# get glyph of this layer
glyph = layer.parent

print(glyph)

for layer in glyph.layers:
	print(layer)
	bg_layer = layer.background
	bg_layer.paths = []
	for path in layer.paths:
		new_path = path.copy()
		bg_layer.paths.append(new_path)
