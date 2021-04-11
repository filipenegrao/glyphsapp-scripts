# MenuTitle: Open all glyphs related to the current comb mark selected.
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

Open all glyphs related to the current comb mark selected.

"""

font = Glyphs.font

# get active layer
layer = font.selectedLayers[0]

# get glyph of this layer
glyph = layer.parent

if glyph.category == "Mark":
	if 'comb' in glyph.name:
		gname = str(glyph.name)
		gname_striped = gname[:-4]
		
		
tab_text = ""

for g in font.glyphs:
	if gname_striped in g.name:
		new_line = "/%s" % g.name
		tab_text += new_line
		print(g.name)
			
if tab_text:
	font.newTab(tab_text)