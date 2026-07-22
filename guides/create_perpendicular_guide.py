# MenuTitle: Create a perpendicular guide from another guide.
# -*- coding: utf-8 -*-

__doc__ = """
Create a perpendicular guide from another guide.
Select a guide and run.
"""

font = Glyphs.font
layer = font.selectedLayers[0]

for guide in layer.guides:
    if guide.selected:
        new_guide = GSGuide()
        new_guide.position = guide.position.x, guide.position.y
        new_guide.angle = guide.angle + 90
        layer.guides.append(new_guide)
