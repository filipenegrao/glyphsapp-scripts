# MenuTitle: Create a center guideline between two guides.
# -*- coding: utf-8 -*-

__doc__ = """
Create a center guideline between two guides.
Select exactly two guides and run.
"""

font = Glyphs.font
layer = font.selectedLayers[0]

selected_guides = [g for g in layer.guides if g.selected]

if len(selected_guides) == 2:
    x1, y1 = selected_guides[0].position.x, selected_guides[0].position.y
    x2, y2 = selected_guides[1].position.x, selected_guides[1].position.y

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
    print("Select exactly two guides first.")
