# MenuTitle: Toggle enumerate node (from first to last)
# -*- coding: utf-8 -*-

__doc__ = """

Toggle between with or without names in nodes by running the script and then pressing OPT + CMD + R.
Please note that the enumeration follows the contours direction, meaning: 
the node with the triangle (that indicates the first anchor) will be the #1.

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


if layer.paths[0].nodes[0].name != None:
    enumerate_nodes(False)
else:
    enumerate_nodes(True)
