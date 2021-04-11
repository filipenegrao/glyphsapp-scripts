# MenuTitle: Open selected glyphs in a new tab
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

Pretty much self explanatory :)

"""

f = Glyphs.font

glyph_str = ''

for glyph in f.selection:
    glyph_str += "/" + glyph.name

# open new tab with text
f.newTab(glyph_str)