#MenuTitle: Create a background's copy to a new layer'.
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__="""

Copy a background to a new layer and open it, so you can compare back and foreground side by side.

"""

font = Glyphs.font
glyphs = font.glyphs

# get active layer
layer = font.selectedLayers[0]
bg_layer = layer.background

# get glyph of this layer
glyph = layer.parent
glyph_name = str(glyph.name)

bg_layer = layer.background
new_layer = GSLayer()
new_layer.name = "background_copy"

# you may set the master ID that this layer will be associated with, otherwise the first master will be used
new_layer.associatedMasterId = font.masters[-1].id # attach to last master
glyph.layers.append(new_layer)

for path in bg_layer.paths:
	new_path = path.copy()
	new_layer.paths.append(new_path)

tab_text = glyph_name*2

if tab_text:
    font.newTab(tab_text)

