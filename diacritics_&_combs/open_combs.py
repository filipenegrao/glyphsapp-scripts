# MenuTitle: Open all comb marks in a new tab
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

Open all comb diacritics in a new tab.

"""

font = Glyphs.font
tab_text = ""
comb = [g.name for g in font.glyphs if g.category == 'Mark' and g.subCategory == 'Nonspacing']

for c in comb:
    new_line = "/%s" % c
    tab_text += new_line

if tab_text:
    font.newTab(tab_text)
