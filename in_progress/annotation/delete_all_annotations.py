# MenuTitle: Delete all annotations in all layers. No undo, so use with precaution.
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Delete all annotations. No undo, so use with precaution.
"""



f = Glyphs.font

for g in f.glyphs:
	for l in g.layers:
		l.annotations = ()
