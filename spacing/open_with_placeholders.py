#MenuTitle: Open selected glyphs with placeholders in a text tab
# -*- coding: utf-8 -*-

__doc__="""
Open a text tab with control characters (e.g., noHO) with all the glyphs selected in the Font View.
"""

from __future__ import division, print_function, unicode_literals


font = Glyphs.font

lc_control = ['n', 'o']
uc_control = ['H', 'O']

selected = font.selection
p = '/Placeholder '

txt = 'nn{0}nnoo{0}oonn{0}oo\nHH{0}HHOO{0}OOHH{0}OO\n'.format(p)

for g in selected:
	txt += '/{}'.format(g.name)
	
font.newTab(txt)