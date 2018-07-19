font = Glyphs.font

# get active layer
layer = font.selectedLayers[0]

# get glyph of this layer
glyph = layer.parent

master_xheight = font.masters[0].xHeight 



def rect_coordinates(px, py, distance):
	d = distance
	return [(px - d, py - d), (px - d, py + d), (px + d, py + d), (px + d, py - d)]


def draw_path(some_layer, list_coord):
    new_path = GSPath()

    for coord in list_coord:
        new_node = GSNode()
        new_node.type = GSLINE
        new_node.position = coord
        new_path.nodes.append(new_node)

    new_path.closed = True
    some_layer.paths.append(new_path)
    some_layer.bezierPath.fill()


def guess_protected_nodes(layer):
	"""
	Get points that have all the characteristics below:
	1) has a "y" value between 0 and x-height (I don't need points that are above or below the x-height)
	2) are curve points, since line points can be changed without much harm
	3) we can ignore off-curve points as well because we want to move them.
	4) finally, we can ignore all the curve points that move towards the x-axis, since we are going to move everything throughout the y-axis.
	"""
	curve_nodes_x = []
	
	for path in layer.paths:
		for node in path.nodes:
			if node.y < 0 or node.y > master_xheight:
# 				print node.y
				continue
			elif node.smooth == True:
# 				print node
				if node.nextNode.x == node.x and node.nextNode.type == "offcurve" or node.x == node.prevNode.x and node.prevNode.type == "offcurve":
						curve_nodes_x.append(node)
	return curve_nodes_x

print "len: ", len(guess_protected_nodes(layer))

list_nodes = guess_protected_nodes(layer)
# print list_nodes

for node in list_nodes:
	another_list = rect_coordinates(node.x, node.y, 10)
	draw_path(layer.background, another_list)

# n_test = layer.paths[0].nodes[11]
# n_test.name = "test" 
# print "node type:", n_test.type, n_test.smooth, n_test.connection
# 	
