# MenuTitle: Diacritics reference
# -*- coding: utf-8 -*-

__doc__ = """

This script creates a visual reference to align diacritics horizontally, based on acute height

"""

from AppKit import NSColor


font = Glyphs.font
up_diacritics = ['dieresiscomb', 'dotaccentcomb', 'gravecomb', 'acutecomb', 'hungarumlautcomb', 'circumflexcomb', 'caroncomb', 'brevecomb', 'ringcomb', 'tildecomb', 'macroncomb']
acute_ref = font.glyphs['acutecomb']
acute_layer = font.glyphs['acutecomb'].layers[0]

# origin x, y
origin_acute = acute_layer.bounds.origin.x, acute_layer.bounds.origin.y

# size w, h 
bounds_acute = acute_layer.bounds.size.width, acute_layer.bounds.size.height

# print origin_acute, bounds_acute

def create_layer(gname, layer_name):
    glyph = font.glyphs[gname]  
    if not glyph.layers[layer_name]:
        new_layer = GSLayer()
        new_layer.name = layer_name
        glyph.layers.append(new_layer)
    else:
        print 'The "{0}" layer already exists.'.format(layer_name)                  
        
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

x1 = 0.0
y1 = origin_acute[1]
y2 = y1 + bounds_acute[1]
# x2 = x1 + bounds_acute[0]


def addGuide(pos_x, pos_y, ang, label=None):
    font = Glyphs.font
    font_master = font.selectedFontMaster
    newGuide = GSGuideLine()
    newGuide.position = pos_x, pos_y
    newGuide.angle = ang
    newGuide.name = label + ': ' + str(pos_y)
    font_master.guides.append(newGuide)


def draw_color(layer, info):
    r, g, b, a = 231 / 255.0, 227 / 255.0, 51 / 147.0, 50 / 100.0
    try:
        NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a).set()
        for gname in up_diacritics:
            l = font.glyphs[d_name].layers['diacritics']
            l.bezierPath.fill()
    except:
        import traceback
        print traceback.format_exc()

for d_name in up_diacritics:
    x2 = x1 + font.glyphs[d_name].layers[0].width
    create_layer(d_name, 'diacritics')
    l = font.glyphs[d_name].layers['diacritics']
    coordinates = ((x1, y1), (x1, y2), (x2, y2), (x2, y1))
    draw_path(l, coordinates)
    addGuide(0.0, y1 + bounds_acute[1]/2, 0.0, 'half acute height')


Glyphs.addCallback(draw_color, DRAWBACKGROUND)
