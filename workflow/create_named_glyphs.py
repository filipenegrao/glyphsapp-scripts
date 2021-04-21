# MenuTitle: (GUI) Create glyphs
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals
from vanilla import *

__doc__ = """

Batch create named glyphs. This is different from Glyph > Add Glyphs 

"""


class BatchGlyphs(object):

    font = Glyphs.font

    def __init__(self):

        self.w = FloatingWindow((400, 150))
        self.w.inputText = TextEditor((20, 20, -20, -80), text="Add the glyphs' names separated by a comma.")
        self.w.openbtn = Button(
            (20, 90, -20, 20), 'Add Glyphs', callback=self.addGlyphs)
        self.w.checkBox = CheckBox((20, 120, -20, 20), 'exportable glyph(s)', value=False)
        self.w.open()


    def createGlyph(self, glyphname):
        if not self.font.glyphs[glyphname]:
            newGlyph = GSGlyph()
            newGlyph.name = glyphname
            newGlyph.export = self.w.checkBox.get()
            f.glyphs.append(newGlyph)
        else:
            return 'There is another glyph called {}.'.format(glyphname)

    def processInputGlyphs(self):
        glyphs = self.w.inputText.get()
        splitedGlyphs = glyphs.split(',')
        return [g.strip(' ') for g in splitedGlyphs]


    def addGlyphs(self, sender):
        gList = self.processInputGlyphs()
        glyphsCreated = ''
        if len(gList) != 0:
            for glyphname in gList:
                self.createGlyph(glyphname)
                glyphsCreated += glyphname
            Message("Glyphs added: {}".format(glyphsCreated) , title="😁")

        else:
            Message("Please, add some glyphs name's first!" , title="😐")

BatchGlyphs()
