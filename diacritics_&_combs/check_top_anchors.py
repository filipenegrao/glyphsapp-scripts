# MenuTitle: [QA] Check top anchors height
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

Check if your top anchors are at the same height as x-height (if it's lowercase) or cap height (uppercases).

"""

f = Glyphs.font
glyphs = f.glyphs

def check_anchor_y():

	tab_text = ""
	
	for glyph in f.glyphs:
		if glyph.subCategory == "Lowercase":
			layer = glyph.layers[font.selectedFontMaster.id]
			xh = layer.master.xHeight
			for anchor in layer.anchors:
				if anchor.name == "top" and anchor.y != xh:
					print(glyph.name, layer.name, anchor.name)
					print(anchor.y, xh)					
					new_line = "/%s" % glyph.name
					tab_text += new_line
		if glyph.subCategory == "Uppercase":
			layer = glyph.layers[font.selectedFontMaster.id]
			caph = layer.master.capHeight
			for anchor in layer.anchors:
				if anchor.name == "top" and anchor.y != caph:
					print(glyph.name, layer.name, anchor.name)
					print(anchor.y, caph)					
					new_line = "/%s" % glyph.name
					tab_text += new_line		
	if tab_text:
		f.newTab(tab_text)

check_anchor_y()
