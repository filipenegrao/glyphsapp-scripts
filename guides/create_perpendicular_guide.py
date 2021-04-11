# MenuTitle: Create a perpendicular guide from another guide.
# -*- coding: utf-8 -*-

__doc__="""

Create a perpendicular guide from another guide. Select a guide and run it.

"""

font = Glyphs.font
glyphs = font.glyphs

# get active layer
layer = font.selectedLayers[0]

# access all guides and pick only the ones that are selected
for guide in layer.guides:
	if guide.selected:
		pos = guide.position.x, guide.position.y
		ang = guide.angle + 90
		new_guide = GSGuideLine()
		new_guide.position = NSPoint(pos[0], pos[1])
		new_guide.angle = ang
		layer.guides.append(new_guide)