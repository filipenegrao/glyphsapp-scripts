#MenuTitle: Disable Auto-Alignment for Selected Glyphs (All Masters)
# -*- coding: utf-8 -*-
"""
Disables automatic alignment for all components in every master layer
of the currently selected glyphs.
"""

from GlyphsApp import Glyphs, GSComponent

font = Glyphs.font

if font is None:
	Glyphs.showMacroWindow()
	print("No font open.")
else:
	# Works both from Font view (grid selection) and Edit view (tab selection)
	if font.currentTab:
		selected_glyphs = set(layer.parent for layer in font.selectedLayers)
	else:
		selected_glyphs = set(font.selection)

	if not selected_glyphs:
		print("No glyphs selected.")
	else:
		font.disableUpdateInterface()
		try:
			count = 0
			for glyph in selected_glyphs:
				for master_layer in glyph.layers:
					for shape in master_layer.shapes:
						if not isinstance(shape, GSComponent):
							continue
						changed = False
						if shape.disableAlignment != True:
							shape.disableAlignment = True
							changed = True
						if hasattr(shape, "automaticAlignment") and shape.automaticAlignment != False:
							shape.automaticAlignment = False
							changed = True
						if changed:
							count += 1
			print("Disabled alignment on %d component(s) across %d glyph(s)." % (count, len(selected_glyphs)))
		finally:
			font.enableUpdateInterface()
