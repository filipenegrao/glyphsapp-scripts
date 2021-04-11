# MenuTitle: Save noHO LSB, RSB and inner counter data to CSV
# -*- coding: utf-8 -*-

__doc__="""

Simple script to get the font metrics and the inner counter of 'n', 'o', 'H', 'O', in order to check the relationship between those values.
It uses the intersectionsBetweenPoints instead of simply getting the LSB and RSB values, so it will potentially ignore serifs when picking up the data.

"""

import csv
import os

font = Glyphs.font
fname = font.familyName
fstyle = font.masters[0].name
foundry = font.manufacturer

path = GetFolder(message='Please, choose a folder to save the file')
fp = path + '/' + 'metrics.csv'

def get_intersections(glyph_name, division):
	g_layer = font.glyphs[glyph_name].layers[0]
	glyph_h = g_layer.paths[0].bounds.size.height
	y_val = glyph_h / division
	intersections = g_layer.intersectionsBetweenPoints((0, y_val), (g_layer.width, y_val))
	lsb = intersections[1].x
	rsb = intersections[5].x - intersections[4].x
	counter = intersections[3].x - intersections[2].x
	values = int(lsb), int(rsb), int(counter)
	return values

metrics_values = {
	'n': get_intersections('n', 2),
	'o': get_intersections('o', 2),
	'H': get_intersections('H', 3),
	'O': get_intersections('O', 2)
}

if os.path.isfile(fp):
	with open(fp, 'a+') as csv_file:
		writer = csv.writer(csv_file)
		if fname and fstyle and foundry:
			writer.writerow([fname + ' ' + fstyle + ' ' + foundry])
			writer.writerow(['glyph', 'LSB', 'RSB', 'COUNTER'])
		for key, value in metrics_values.items():
			writer.writerow([ key, value[0], value[1], value[2] ])
			writer.writerow([ '%', value[0] / value[2], value[1] / value[2] ])
		Message('😎', 'Info added to \n {}'.format(path))
else:
	with open(fp, 'w') as csv_file:
		writer = csv.writer(csv_file)
		if fname and fstyle and foundry:
			writer.writerow([fname + ' ' + fstyle + ' ' + foundry])
			writer.writerow(['glyph', 'LSB', 'RSB', 'COUNTER'])
		for key, value in metrics_values.items():
			writer.writerow([key, value[0], value[1], value[2]])
			writer.writerow(['%', value[0] / value[2], value[1] / value[2]])
		Message('😎', 'File successfully saved to \n {}'.format(path))


	

# with open(path + '/' + 'metrics.csv', 'a+') as csv_file:
# 	writer = csv.writer(csv_file)
# 	if fname and fstyle and foundry:
# 		writer.writerow([fname + ' ' + fstyle + ' ' + foundry])
# 	writer.writerow(['glyph', 'LSB', 'RSB', 'COUNTER'])
# 	for key, value in metrics_values.items():
# 		writer.writerow([ key, value[0], value[1], value[2] ])
# 		writer.writerow([ '%', value[0] / value[2], value[1] / value[2] ])
# 	Message('😎', 'File successfully saved to \n {}'.format(path))
