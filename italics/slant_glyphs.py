#MenuTitle: Slant Glyphs
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals


__doc__="""

(GUI) This tool is build to slant all selected glyphs in Edit View while adds a copy of the roman version in the background.
It's not supposed to be an automatic italic solution but gives you a head start.
** Warning: ** this script erases all the layers in the background that wore previously there.
Comment the following line to avoid that: background_layer.paths = []

"""
import copy
import math
import traceback
from vanilla import *
from AppKit import *


class GlyphSlanter(object):
	"""docstring for GlyphSlanter."""

	def __init__(self):
		super(GlyphSlanter, self).__init__()

# 1. USER INTERFACE

		self.w = Window((250, 280), "Slant Glyphs")

		self.w.slant_label = TextBox((20, 20, -100, 20), u"Slant (°)", alignment = "right")
		self.w.slant = EditText((160, 20, -20, 20), placeholder = "0")
		self.w.width_label = TextBox((20, 50, -100, 20), "Width (%)", alignment = "right")
		self.w.width = EditText((160, 50, -20, 20), placeholder = "100")
		self.w.height_label = TextBox((20, 80, -100, 20), "Height (%)", alignment = "right")
		self.w.height = EditText((160, 80, -20, 20), placeholder = "100")
		self.w.color_label = TextBox((20, 115, -100, 20), "Background Color", alignment = "right")
		self.w.color_well = ColorWell((160, 110, -20, 30),
							color = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.93, 0.95, 0.92, 1.0))
		self.w.selected_glyphs = Button((20, 175, -20, 20), "Change Selected Glyphs", callback = self.selected_glyphs_callback)
		self.w.change_color_callback = Button((20, 205, -20, 20), "Change Background Color", callback = self.change_color_callback)
		self.w.add_guide_callback = Button((20, 235, -20, 20), "Add Angle Guideline", callback = self.add_guide_callback)

		self.w.open()

# 2. GETTERS

	def get_angle(self):
		try:
			if len(self.w.slant.get()) == 0:
				return 0.0
			else:
				return float(self.w.slant.get())
		except Exception as e:
			raise e

	def get_horizontal(self):
		try:
			if len(self.w.width.get()) == 0:
				return 1.0
			else:
				return float(self.w.width.get()) / 100.0
		except Exception as e:
			raise e

	def get_vertical(self):
		try:
			if len(self.w.height.get()) == 0:
				print(1.0)
				return 1.0
			else:
				return float(self.w.height.get()) / 100.0
		except Exception as e:
			raise e

	def get_color(self):
		try:
			if type(self.w.color_well.get()) == NSCalibratedRGBColor:
				rgba_float = [0.93, 0.95, 0.92, 1.0] # dafault value
				return rgba_float
			else:
				RGBA = self.w.color_well.get()
				print(RGBA)
				rgba_str = str(RGBA)
				rgba_str = rgba_str.replace('sRGB IEC61966-2.1 colorspace ', '')
				rgba_str = rgba_str.split(' ')
				rgba_float = [float(i) for i in rgba_str]
				return rgba_float
		except Exception as e:
			raise e

# 3. SETTERS

	def draw_guide(self, angle):
		try:
			for layer in Glyphs.font.selectedLayers:
				new_guide = GSGuideLine()
				new_guide.position = 0, 0
				new_guide.angle = 90.0 - angle
				new_guide.name = str(angle) + u'°'
				layer.guides.append(new_guide)
		except Exception as e:
			raise e

	def coloring_background(self, layer, info):
		# get RGBA colors from def get_color
		color_rgba = self.get_color()
		print(color_rgba)
		R, G, B, A = color_rgba
		try:
			NSColor.colorWithCalibratedRed_green_blue_alpha_(R, G, B, A).set()
			layer.background.bezierPath.fill()
		# Error. Print exception.
		except Exception as e:
			raise e
			print(traceback.format_exc())

	def copy_fore2background(self):
		# iterate all paths and append them into the list of paths.
		try:
			for layer in Font.selectedLayers:
				background_layer = layer.background
				background_layer.paths = []
				for path in layer.paths:
					new_path = path.copy()
					background_layer.paths.append(new_path)
		except Exception as e:
			raise e

	def matrix(self, angle, horizontal, vertical):
		try:
			for layer in Glyphs.font.selectedLayers:
				layer.applyTransform([
						horizontal, # x scale factor
						0.0, # x skew factor
						math.radians(angle), # y skew factor
						vertical, # y scale factor
						0.0, # x position
						0.0  # y position
						])
		except Exception as e:
			raise e

# BUTTONS CALLBACKS

	def selected_glyphs_callback(self, sender):
		a = self.get_angle()
		h = self.get_horizontal()
		v = self.get_vertical()
		self.copy_fore2background()
		self.matrix(a, h, v)
		Glyphs.redraw()

	def add_guide_callback(self, sender):
		a = self.get_angle()
		self.draw_guide(a)

	def change_color_callback(self, sender):
		Glyphs.addCallback(self.coloring_background, DRAWBACKGROUND)


GlyphSlanter()
