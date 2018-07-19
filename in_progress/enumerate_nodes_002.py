# MenuTitle: Toggle enumerate node (from "Glyphs order")
# -*- coding: utf-8 -*-

__doc__ = """

Toggle between with or without names in nodes by running the script and then pressing OPT + CMD + R.
Please notice that the enumeration starts at the previous node as the first 'moveTo' operation on the path.
More about on https://forum.glyphsapp.com/t/order-of-nodes-starts-at-second-node/3737/3

"""


f = Glyphs.font

layer = f.selectedLayers[0]
g = layer.parent

def enumerate_nodes(put_numbers = True):
    if put_numbers:
        for path in layer.paths:
            for i, node in enumerate(path.nodes):
                node.name = str(i)
    else:
        # ==> clear all node names: <==
        for path in layer.paths:
            for node in path.nodes:
                node.name = None


if layer.paths[0].nodes[0].name != None:
    enumerate_nodes(False)
else:
    enumerate_nodes(True)
