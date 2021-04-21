#MenuTitle: For each master, create a less glyph from a greater component
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__="""

For each master, create a less glyph from a greater component.
It will be update in the future to auto rotate the component.

"""

font = Glyphs.font
glyphs = font.glyphs

comp_layer = font.glyphs['less'].layers

for l in comp_layer:
	l.components.append(GSComponent('greater'))
	l.LSB = font.glyphs['greater'].layers[font.selectedLayers[0].layerId].LSB
	l.RSB = font.glyphs['greater'].layers[font.selectedLayers[0].layerId].LSB