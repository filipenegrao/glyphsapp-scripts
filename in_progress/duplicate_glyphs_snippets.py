from __future__ import print_function

from copy import copy
font = Glyphs.font

current_layer = Glyphs.font.selectedLayers[0] # current layer
bg = current_layer.background
fmaster = font.masters[0]
glyph = current_layer.parent

l1 = font.glyphs['O'].layers[0]
l2 = font.glyphs['Q'].layers[0]
l2bg = l2.background



def glyph_exists(gname):
	glyph_existence = False
	if gname in font.glyphs:
		glyph_existence = True
	return glyph_existence


def _duplicate_glyph(glyph, suffix=None):
	new_glyph = glyph.copy()
	new_glyph.name = glyph.name + suffix
	font.glyphs.append(new_glyph)


def duplicate_glyph(glyph, suffix):
	if not glyph_exists(glyph.name + suffix):
		_duplicate_glyph(glyph, suffix)
		print("Glyph %s was created." % (glyph.name + suffix))
	else:
		print("Glyph %s already exists." % (glyph.name + suffix))


def paths_to_layer(layer1, layer2):
	layer2.paths = copy(layer1.paths)
	print("%s's paths were copy to %s" % (layer1.parent.name, layer2.parent.name))


# duplicate_glyph(glyph, ".002")
# paths_to_layer(l1, l2)

O_regular = glyph.layers["Regular"]
O_bold = glyph.layers["Bold"]

print(R_bold)
# paths_to_layer(O_regular, O_bold)