#MenuTitle: Delete all anchors from the current glyph
# -*- coding: utf-8 -*-

__doc__="""

Remove all anchors from current, selected, glyph.

"""

font = Glyphs.font

layer = font.selectedLayers[0]
glyph = layer.parent

for anchor in layer.anchors:
	print ("Deleting %s from %s" % (anchor.name, glyph.name))
	# delete anchor
	del(layer.anchors[anchor.name]) 
