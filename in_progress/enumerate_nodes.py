# MenuTitle: Enumerate nodes
# -*- coding: utf-8 -*-

__doc__ = """

Add a name to all nodes that are equivalent of a number, in sequence...
so, the first node (the one with the triangle) will receive the number 1 and so on.

To delete all the names, just change the last line of this script to
enumerate_nodes(False). 

An GUI will be add later.

"""


f = Glyphs.font

layer = f.selectedLayers[0]
g = layer.parent


def enumerate_nodes(put_numbers = True):
	if put_numbers:
		for path in layer.paths:
			# the first node is the last in index
			first_node = path.nodes[-1]

			# define the number wich the enumaration will start
			x = 1
			for node in path.nodes:
				node.name = str(x + 1)
				x += 1

			# after applying the name for each point in order,
			# we change the last point in index to '1'
			first_node.name = '1'
	else:
		# ==> clear all node names: <==
		for path in layer.paths:
			for node in path.nodes:
				node.name = None

enumerate_nodes()
