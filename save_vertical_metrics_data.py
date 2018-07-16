# MenuTitle: Save vertical metrics data
# -*- coding: utf-8 -*-

__doc__="""

This script checks the vertical metrics data of an open font and saves in a .csv file.
The default file name is set to vertical_proportions.csv. To change that, just edit this line:
file_path = folder_path + '/vertical_proportions.csv' 

"""

import os.path
import csv

font = Glyphs.font


def max_y(glyph_name):
    aglyph = font.glyphs[glyph_name].layers[0]
    p_nodes = []
    for path in aglyph.paths:
        for node in path.nodes:
            p_nodes.append(node.position.y)
    return max(p_nodes)


def min_y(glyph_name):
    aglyph = font.glyphs[glyph_name].layers[0]
    p_nodes = []
    for path in aglyph.paths:
        for node in path.nodes:
            p_nodes.append(node.position.y)
    return min(p_nodes)


b = font.glyphs['b'].layers[0]
p = font.glyphs['p'].layers[0]
o = font.glyphs['o'].layers[0]
x = font.glyphs['x'].layers[0]
H = font.glyphs['H'].layers[0]
O = font.glyphs['O'].layers[0]
l = font.glyphs['l'].layers[0]
x_h = x.bounds.size.height
o_h = o.bounds.size.height + o.bounds.origin.y
b_h = max_y('b')
p_h = p.bounds.origin.y
lc_overshoot = o.bounds.size.height + o.bounds.origin.y - x.bounds.size.height
H_h = H.bounds.size.height
O_h = O.bounds.size.height + O.bounds.origin.y
uc_overshoot = O.bounds.size.height + O.bounds.origin.y - H.bounds.size.height

# coordinates for /l
x1, y1 = 0, font.masters[0].xHeight / 2
x2, y2 = l.width, y1

# intersections
intersections_l = l.intersectionsBetweenPoints((x1, y1), (x2, y2))

# stroke width based on intersections
swl = intersections_l[2].x - intersections_l[1].x

header = []
header.append(('font', 'name', 'designer', 'foundry', 'year', 'basic stroke width (/l)', 'descender', 'x-height', 'cap height', 'ascender', 'overshoot lowercases', 'overshoot uppercases', 'UPM', 'metrics: descender', 'metrics: x-height', 'metrics: cap height', 'metrics: ascender', 'descender - metrics descender', 'ascender - metrics ascender'))


folder_path = GetFolder(message="Save file at", allowsMultipleSelection = False)
file_path = folder_path + '/vertical_proportions.csv'

try:
    if not os.path.isfile(file_path):
        with open(file_path, 'a') as fh1:
            writer = csv.writer(fh1)
            writer.writerows(header)
    fontdata = []

    for f in font.masters:
        fontdata.append((font.familyName, f.name, font.designer, font.manufacturer, font.date.year, swl, p_h, x_h, H_h, b_h, lc_overshoot, uc_overshoot, font.upm, f.descender, f.xHeight, f.capHeight, f.ascender, f.descender - p_h, f.ascender - b_h))
        with open(file_path, 'a') as fh2:
            writer = csv.writer(fh2)
            writer.writerows(fontdata)

    print("Writing complete for %s %s" % (font.familyName, f.name))

except Exception as e:
    raise e
    Glyphs.showMacroWindow()
