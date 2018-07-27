# MenuTitle: Cut selection in half (horizontaly)
# -*- coding: utf-8 -*-

__doc__ = """


"""

font = Glyphs.font

# get active layer
layer = font.selectedLayers[0]

# get glyph of this layer
glyph = layer.parent

x = layer.selectionBounds.origin.x
y = layer.selectionBounds.origin.y
w = layer.selectionBounds.size.width
h = layer.selectionBounds.size.height

layer.cutBetweenPoints(NSPoint(x+w/2, y+h), NSPoint(x+w/2, y))

