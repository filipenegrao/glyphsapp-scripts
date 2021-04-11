from __future__ import print_function
from AppKit import NSColor

font = Glyphs.font
# layer = font.selectedLayers[0]

LAYER_NAME = 'xheigth-plugin-w'

XH = font.masters[0].xHeight
AH = font.masters[0].ascender
DH = font.masters[0].descender

HALF_XH = int(XH / 2)
T = 30  # the tolerance, that needs to adapt for each font
RAISE_AMOUNT = 10

# rect cordinates
x1 = 0
x2 = None  # This value will be defined in initial_safezone()
y1 = HALF_XH - T
y2 = HALF_XH + T

# Colors
r, g, b, a = 133 / 255.0, 203 / 255.0, 51 / 255.0, 50 / 80.0



def create_new_layer(layer_name):
    """
    Works on the active tab with selected glyphs.

    This function takes a str (layer_name) and check if there is a layer with
    this name. If the layer doesn't exists, then creates a new layer.

    """

    for glyph in font.glyphs:
        for layer in glyph.layers:
            if layer in Font.selectedLayers:
                print(layer)
                if not glyph.layers[layer_name]:
                    new_layer = GSLayer()
                    new_layer.name = layer_name
                    glyph.layers.append(new_layer)
                else:
                    print('The "{0}" layer already exists.'.format(layer_name))



def draw_ground(layer, info):
    # Due to internal Glyphs.app structure, we need to catch and print exceptions
    # of these callback functions with try/except like so:
    try:
        NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a).set()
        layer.background.bezierPath.fill()  # check how to draw on foreground
    except:
        import traceback
        print(traceback.format_exc())


def draw_path(some_layer, list_coord):
    newPath = GSPath()

    for coord in list_coord:
        newNode = GSNode()
        newNode.type = GSLINE
        newNode.position = coord
        newPath.nodes.append(newNode)

    newPath.closed = True
    some_layer.paths.append(newPath)
    some_layer.bezierPath.fill()

    # add your function to the hook
    Glyphs.addCallback(draw_ground, DRAWINACTIVE)


def initial_safezone(some_layer):

    """
    Get all selected layers and it's respective width.
    The width will be used to draw a safe zone area at the background

    """

    # for layer in Font.selectedLayers:
    glyph = layer.parent
    gname = glyph.name
    gwidth = font.glyphs[gname].layers[0].width
    x2 = gwidth

    current_glyph_list = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
    draw_path(some_layer, current_glyph_list)


def main():
    for glyph in font.glyphs:
        for layer in glyph.layers:
            if layer in Font.selectedLayers:
                print(layer)
                n_layer = create_new_layer(LAYER_NAME)
                initial_safezone(n_layer)

main()

"""
Traceback (most recent call last):
  File "<string>", line 105, in <module>
  File "<string>", line 103, in main
  File "<string>", line 94, in initial_safezone
  File "<string>", line 72, in draw_path
AttributeError: 'NoneType' object has no attribute 'paths'
"""