# MenuTitle: Create a center guideline between two points.
# -*- coding: utf-8 -*-

__doc__ = """
Create a guideline at the center between two selected nodes.
Select exactly two nodes and run.
"""

font = Glyphs.font
layer = font.selectedLayers[0]

my_nodes = [node for path in layer.paths for node in path.nodes if node.selected]

if len(my_nodes) == 2:
    x1, y1 = my_nodes[0].x, my_nodes[0].y
    x2, y2 = my_nodes[1].x, my_nodes[1].y

    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    ang = 90.0 if dx >= dy else 0.0

    newGuide = GSGuide()
    newGuide.position = cx, cy
    newGuide.angle = ang
    layer.guides.append(newGuide)
else:
    print("Select exactly two nodes first.")
