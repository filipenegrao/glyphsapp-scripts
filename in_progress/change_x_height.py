from __future__ import print_function
from AppKit import NSColor

font = Glyphs.font
layer = font.selectedLayers[0]

background_layer = layer.background
background_layer.paths = []

# ----------------

def drawGlyphIntoBackground(layer, info):

        # Due to internal Glyphs.app structure, we need to catch and print exceptions
        # of these callback functions with try/except like so:
        try:
        	# Your drawing code here
        	NSColor.yellowColor().set()
        	layer.background.bezierPath.fill()

        # Error. Print exception.
        except:
        	import traceback
        	print(traceback.format_exc())

# add your function to the hook
Glyphs.addCallback(drawGlyphIntoBackground, DRAWBACKGROUND)

# ----------------

# find the middle of the x-height
xh = font.masters[0].xHeight
half_xh = int(xh / 2)
tolerance = 30  # the tolerance needs to adapt for each font
t = tolerance
raise_amount = 10

# set reference values
## every point bellow p's bound origin won't move
p = font.glyphs['p'].layers[0]
p_origin_y = p.bounds.origin.y  

## every point above h's bound height won't move, including this value
h = font.glyphs['h'].layers[0]
h_h = h.bounds.size.height

o = font.glyphs['o'].layers[0]

coor_x1 = 0
coor_x2 = o.width
coor_y1 = half_xh - tolerance
coor_y2 = half_xh + tolerance

# ----------------

newPath = GSPath()
nu_nodes = [(coor_x1, coor_y1), (coor_x1, coor_y2), (coor_x2, coor_y2), (coor_x2, coor_y1)]

for n in nu_nodes:
	newNode = GSNode()
	newNode.type = GSLINE
	newNode.position = n
	newPath.nodes.append(newNode)

newPath.closed = True
background_layer.paths.append(newPath)

NSColor.yellowColor().set()
layer.background.bezierPath.fill()


def glyphs_width():
	node_coor = {}
	for layer in Font.selectedLayers:
		glyph = layer.parent
		gname = glyph.name
		node_coor[gname] = font.glyphs[gname].layers[0].width
	return node_coor

Glyphs.addCallback(drawGlyphIntoBackground, DRAWBACKGROUND)