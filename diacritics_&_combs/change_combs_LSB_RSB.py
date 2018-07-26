#MenuTitle: Change the LSB and RSB for all comb glyphs
# -*- coding: utf-8 -*-

__doc__="""

Change the LSB and RSB for all comb glyphs. Default value is set to 50, but can be changed in line 24-25.
I was too lazy to add an GUI for this simple script.

"""


font = Glyphs.font

print ""
print "=" * 46
print "The following sidebearing's combs were changed"
print "=" * 46
print ""

for glyph in font.glyphs:
	for layer in glyph.layers:
		if "comb" in glyph.name:
			layer.LSB = 50
			layer.RSB = 50
			print "%s %s --> LSB = %s | RSB = %s" % (layer.name, glyph.name, layer.LSB, layer.RSB)

Glyphs.showMacroWindow()