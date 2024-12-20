# MenuTitle: Change X-Height
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

Working on this one.
(GUI) No doc at the moment.
**Pro tip:** Use Arrows Up and Down as shortcuts.

"""


from AppKit import NSColor
from purenudge import nudgeMove

font = Glyphs.font

LAYER_NAME = "xheigth-plugin-w"

XH = font.masters[0].xHeight
AH = font.masters[0].ascender
DH = font.masters[0].descender


HALF_XH = int(XH / 2)
T = 20  # the tolerance, that needs to adapt for each font
RAISE_AMOUNT = 10


def draw_color(layer, info):
    r, g, b, a = 231 / 255.0, 227 / 255.0, 51 / 147.0, 50 / 100.0
    try:
        NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a).set()
        layer.background.bezierPath.fill()
    except:
        import traceback

        print(traceback.format_exc())


def create_new_layer(layer_name):
    for glyph in font.glyphs:
        for layer in glyph.layers:
            if layer in Font.selectedLayers:
                print(layer)
                if not glyph.layers[layer_name]:
                    new_layer = GSLayer()
                    new_layer.name = layer_name
                    glyph.layers.append(new_layer)
                else:
                    print(f'The "{layer_name}" layer already exists.')


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


def initial_safezone_vertical(point1, point2):
    gname = glyph.name
    x1, x2 = point1, point2
    x1 -= T
    x2 += T
    y1 = DH
    y2 = AH

    bg = layer.background

    print(gname, ((x1, y1), (x1, y2), (x2, y2), (x2, y1)))
    current_glyph_list = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
    draw_path(bg, current_glyph_list)


def initial_safezone_horizontal(point1, point2):
    gname = glyph.name
    y1, y2 = point1, point2
    y1 -= T
    y2 += T
    gwidth = font.glyphs[gname].layers[0].width
    x2 = gwidth
    x1 = 0

    bg = layer.background

    # print gname, ((x1, y1), (x1, y2), (x2, y2), (x2, y1))
    current_glyph_list = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
    draw_path(bg, current_glyph_list)


def list_points():
    """
    This function will ignore OFFCURVE points,
    since we only need to compare the ONCURVE or LINE points.
    Returns a Tuple with two lists: xlist and ylist.
    """
    xlist = []
    ylist = []

    for path in layer.paths:
        for node in path.nodes:
            if node.type != OFFCURVE:
                xlist.append(node.x)
                ylist.append(node.y)

    return sorted(xlist), sorted(ylist)


def find_closest_points(a_list, a_number, num_of_points):
    """
    some_list -> (list of ints) A list of x or y coordinates
    a_number -> (int) a specific number that will be our base
    num_of_points -> (int) how many numbers we should looking for
    """
    if not a_list:  # Verifica se a lista está vazia
        print("🚨 Warning: empty list of closest points.")
        return []

    closest_points = []

    while num_of_points > 0 and a_list:
        closest_num = min(a_list, key=lambda x: abs(x - a_number))
        closest_points.append(closest_num)
        a_list.remove(closest_num)
        num_of_points -= 1

    return closest_points


Glyphs.clearLog()

for glyph in font.glyphs:
    for layer in glyph.layers:
        if layer in Font.selectedLayers:

            list_y = list_points()[1]
            W_HALF = layer.bounds.size.width / 2
            py1, py2 = find_closest_points(list_y, W_HALF, 2)
            initial_safezone_horizontal(py1, py2)

            list_x = list_points()[0]
            px1, px2 = find_closest_points(list_x, HALF_XH, 2)
            initial_safezone_vertical(px1, px2)


Glyphs.addCallback(draw_color, DRAWFOREGROUND)
# Glyphs.addCallback(draw_color, DRAWINACTIVE)
Glyphs.showMacroWindow()
