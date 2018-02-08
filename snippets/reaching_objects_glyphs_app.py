print " "
print "-" * 150
print "# GSAplicattion"
print Glyphs

print " "
print "-" * 150
print "# All open Fonts"
print Glyphs.fonts

print " "
print "-" * 150
print "# Current Fonts"
print Glyphs.font

print " "
print "-" * 150
print "# All Glyphs of All open Fonts"
for font in Glyphs.fonts:
	for glyph in Glyphs.font.glyphs:
		print glyph

print " "
print "-" * 150
print "# All Glyphs of current Font"
print Glyphs.font.glyphs

print " "
print "-" * 150
print "# All layers of all open fonts"
for font in Glyphs.fonts:
	for glyph in Glyphs.font.glyphs:
		print glyph

print " "
print "-" * 150
print "# Current layer"
print Glyphs.font.selectedLayers[0]
