# MenuTitle: Create a center guideline between two points.
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from Foundation import NSPoint


__doc__="""

Create a guideline guideline between two points.

"""

f = Glyphs.font
glyphs = f.glyphs
layer = Glyphs.font.selectedLayers[0] # current layer


my_nodes = []

for path in layer.paths:
	for node in path.nodes:
		if node.selected:
			my_nodes.append(node)
			
def average(number1, number2):
	return (number1 + number2) / 2.0

ang = 0.0

if len(my_nodes) == 2:
	x1 = my_nodes[0].x
	y1 = my_nodes[0].y
	
	x2 = my_nodes[1].x
	y2 = my_nodes[1].y
	
	x3 = average(x1, x2)
	y3 = average(y1, y2)
	
	x4 = x1 - x2
	y4 = y1 - y2

	if x4 == max((abs(x4)), (abs(y4))):
		ang = 90.0
		
else:
	print("Select two nodes first (and only two!)")

## add guideline
newGuide = GSGuideLine()
newGuide.position = NSPoint(x3, y3)
newGuide.angle = ang
layer.guides.append(newGuide)
# Glyphs.showMacroWindow()
