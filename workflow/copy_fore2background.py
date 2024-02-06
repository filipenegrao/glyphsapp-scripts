#MenuTitle: Copy glyph's foregrounds to backgrounds.
# -*- coding: utf-8 -*-

__doc__="""

Copy Master's foregrounds to its respective backgrounds.
Just a quick way to do a copy, when you need to modify all the masters of a glyph.
** Warning: ** this script erases the background layer's paths that wore previously there.
Comment the following line to avoid that: bg_layer.paths = []

"""


glyph = layer.parent

def remove_masters_backgrounds(glyph):
	for layer in glyph.layers:
		if layer.isMasterLayer:
			layer.background = None
			
def add_foreground_to_bg(glyph):
	for layer in glyph.layers:
		if layer.isMasterLayer:
			layer.background = layer.copy()

remove_masters_backgrounds(glyph)
add_foreground_to_bg(glyph)
Font.newTab(glyph.name)