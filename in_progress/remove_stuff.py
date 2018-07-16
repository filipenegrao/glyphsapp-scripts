
font = Glyphs.font

current_layer = Glyphs.font.selectedLayers[0] # current layer
bg = current_layer.background
fmaster = font.masters[0]
glyph = layer.parent


def remove_paths(layer):
    for path in layer.paths:
        del(layer.paths[0])


def remove_local_guides(layer):
    layer.guides = []


def remove_golbal_guides(a_master):
    a_master.guides = []


def remove_sb(layer):
    layer.LSB, layer.RSB = 0, 0


def remove_kerning():
    pass


def remove_colors(glyph):
    glyph.color = 9223372036854775807


def remove_notes(layer):
    layer.annotations = []


def remove_background_image(layer):
    layer.backgroundImage = None


# remove_paths(layer)
# remove_local_guides(layer)
# remove_golbal_guides(a_master)
# remove_sb(layer)
# remove_colors(glyph)
# remove_notes(current_layer)
# remove_background_image(current_layer)
