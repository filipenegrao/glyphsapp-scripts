#MenuTitle: Make it thinner
# -*- coding: utf-8 -*-

__doc__="""

(GUI) This script export all open fonts (instances inside fonts, to be precise) to a selected folder.
The default folder is configured to ~/Library/Application Support/Adobe/Fonts.
Vanilla required.

A ideia é:

1) achar o tamanho das hastes na vertical e na horizontal, usando
layer.intersectionsBetweenPoints
2) mover o lado esquerdo da haste para dentro (+)
3) mover o lado esquerdo para fora (-)

"""

layer = Glyphs.font.selectedLayers[0] # current layer

# show all intersections with glyph at y = 350
intersections = layer.intersectionsBetweenPoints((0, 350), (layer.width, 350))
# print intersections
# print layer.width

# left sidebearing at measurement line
print intersections[1].x
left_space = intersections[1].x
print left_space

# right sidebearing at measurement line
print layer.width - intersections[-2].x
right_space = layer.width - intersections[-2].x
print right_space

stem_horizontal =  layer.width - left - right
print stem_horizontal

x_middle = left_space + stem_horizontal / 2
print x_middle

x_height = layer.glyphMetrics()[4]
cap_height = layer.glyphMetrics()[2]
angle = layer.glyphMetrics()[5]
print x_height

# access all selected nodes
for path in layer.paths:
        for node in path.nodes:
			# print node.selected
            # do something with selected nodes
            if node.selected:
            	# print 'x: ' + str(node.x), 'y: ' + str(node.y)
            	selected_nodes_x.append(node.x)

            	if node.x <= 105.0:
            		pass
            		# node.x += 10
            	else:
            		pass
            		# node.x -= 10
