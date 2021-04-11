f = CurrentFont()
g = CurrentGlyph()

layer = Glyphs.font.selectedLayers[0] # current layer


def draw_circle(xxx_todo_changeme, diameter):
	(origin_x, origin_y) = xxx_todo_changeme
	pen = g.getPen()
	
	d = diameter  #diameter
	r = d / 2  #radius
	h = r * 0.55229 #handle size
	x0, y0 = origin_x, origin_y #origin
	#since the pen starts at the first oncurve point, it needs to add a radius value to 'correct' the initial point
	x_init = r + origin_x 
	y_init = origin_y - r
	
	# oncurve points
	x1, y1 = x_init, y_init
	x2, y2 = x1 + r, y1 + r
	x3, y3 = x1, y2 + r
	x4, y4 = x3 - r, y2 

	pen.moveTo((x1, y1))
	pen.curveTo((x1+h,y1), (x2,y2-h), (x2,y2))
	pen.curveTo((x2,y2+h), (x3+h,y3), (x3,y3))
	pen.curveTo((x3-h,y3), (x4,y4+h), (x4,y4))
	pen.curveTo((x4,y4-h), (x1-h,y1), (x1,y1))
	pen.closePath()
	
	g.update()

# show all intersections with glyph at y=100
# intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width+1000, 100))
# print(intersections)
# 
# # left sidebearing at measurement line
# print(intersections[1].x)
# 
# # right sidebearing at measurement line
# print(layer.width - intersections[-2].x)


# find the the x-height's middle point
font = Glyphs.font
selected_master = font.selectedFontMaster
x = selected_master.xHeight
half_x = x/2

# show all intersections with the glyph at y = half_x
intersections = layer.intersectionsBetweenPoints((-1000, half_x), (layer.width+1000, half_x))


# print len(intersections)

# ip = intersections[1].x, intersections[1].y
# sz = intersections[2].x - intersections[1].x

li = [] # list of intersections (excluding the lsb and rsb)

for i in range(len(intersections)):
	if i == 0 or i == len(intersections)-1:
		continue
	else:
		li.append((intersections[i].x, intersections[i].y))
		
new_list = zip(li,li[1:])[::2]
 
for v in range(len(new_list)):
	p1 = new_list[v][0][0]
	p2 = new_list[v][1][0] - p1
	draw_circle(new_list[v][0], p2)
	