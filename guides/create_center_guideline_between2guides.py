# MenuTitle: Create a center guideline between two guides.
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals
from Foundation import NSPoint

__doc__="""

Create a center guideline between two guides.

"""

font = Glyphs.font
glyphs = font.glyphs

# get active layer
layer = font.selectedLayers[0]


def average(number1, number2):
	return (number1 + number2) / 2.0

selected_guides = []

# access all guides and pick only the ones that are selected
for guide in layer.guides:
	if guide.selected:
		selected_guides.append(guide)

ang = 0.0

if len(selected_guides) == 2:
	x1 = selected_guides[0].x
	y1 = selected_guides[0].y
	
	x2 = selected_guides[1].x
	y2 = selected_guides[1].y
	
	x3 = average(x1, x2)
	y3 = average(y1, y2)
	
	x4 = x1 - x2
	y4 = y1 - y2

	if x4 == max((abs(x4)), (abs(y4))):
		ang = 90.0
		
else:
	print("Select two guides first (and only two...)")



## add guideline
newGuide = GSGuideLine()
newGuide.position = NSPoint(x3, y3)
newGuide.angle = ang
layer.guides.append(newGuide)
# Glyphs.showMacroWindow()
