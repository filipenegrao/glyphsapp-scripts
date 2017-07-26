#MenuTitle: Add label to selected guideline
# -*- coding: utf-8 -*-

__doc__="""
Add label to selected guideline.
"""

# encoding: utf-8

from GlyphsApp.plugins import *
from vanilla import *

# This script is based on Georg Seifert's code available on:
# https://forum.glyphsapp.com/t/feature-suggestion-guideline-label/1809/8

# Select one guide
# Glyphs 2.3
# label_name = ""
# Layer.selection[0].name = "teste" + " | angle: " + str(Layer.selection[0].angle)
# print str(Layer.selection[0].angle)
# print "Done!"

# or Glyphs 2.2
# Font.selectedLayers[0].selection[0].name = "Hallo"

class WindowLabel(object):
	def __init__(self):
		self.w = vanilla.Window((300, 100), "Add Label")
		self.w.editText = EditText((10, 10, -10, 22), "name", sizeStyle='small', callback=self.editTextCallback)
		self.w.myButton = vanilla.Button((10, 40, -10, 20), "add", sizeStyle='small', callback=self.nameLabel)
		self.w.open()
		self.w.makeKey()

	def editTextCallback(self, sender):
		sender.get()

	def nameLabel(self, sender):
		label_name = (self.w.editText.get())
        Layer.selection[0].name = label_name
		print "label add to selected guideline: " + label_name

WindowLabel()
