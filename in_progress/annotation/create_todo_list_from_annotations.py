# MenuTitle: Create to-do list from annotations.
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

in progress

"""

f = Glyphs.font

for g in f.glyphs:
	for l in g.layers:
		if l.annotations == TEXT:
			print(l.annotations.text)

Glyphs.showMacroWindow()