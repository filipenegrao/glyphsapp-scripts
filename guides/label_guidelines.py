#MenuTitle: Label Guidelines
# -*- coding: utf-8 -*-
__doc__="""

(GUI) Label Guidelines was written to (obviously) add labels to Guidelines.
Additionally, it has the option to delete all guides (local or global). Vanilla required.

"""

import GlyphsApp
from vanilla import *


class LabelerWindow(object):
    """docstring for LabelerWindow"""

    def __init__(self):
        super(LabelerWindow, self).__init__()

        self.w = Window((300, 200), "Label Guidelines")
        self.w.box = Box((10, 10, -10, 80))
        self.w.box.txt = TextBox((10, 10, -20, 20), "Label name: ")
        self.w.box.editText = EditText((100, 10, -10, 20))
        self.w.box.btn_add_label = Button((100, 40, -10, 20), "Add Label",callback=self.buttonAddLabelCallback)
        self.w.btn1 = Button((114, 100, -24, 20), "Add metrics guides", callback=self.addGuideMetricsCallback)
        self.w.btn2 = Button((114, 130, -24, 20), "Clear all global guides", callback=self.deleteGlobalCallback)
        self.w.btn3 = Button((114, 160, -24, 20), "Clear local guides", callback=self.deleteLocalCallback)
        self.w.open()

    def addGuide(self, pos_x, pos_y, ang, label=None):
        font = Glyphs.font
        font_master = font.selectedFontMaster
        newGuide = GSGuideLine()
        newGuide.position = pos_x, pos_y
        newGuide.angle = ang
        newGuide.name = label + ': ' + str(pos_y)
        font_master.guides.append(newGuide)

    def getDimensionsValues(self):
        font = Glyphs.font
        metrics_dict = {
            'x_height': font.selectedFontMaster.xHeight,
            'ascender': font.selectedFontMaster.ascender,
            'descender': font.selectedFontMaster.descender,
            'cap_height': font.selectedFontMaster.capHeight
        }

        return metrics_dict

    def buttonAddLabelCallback(self, sender):
        try:
            if len(Layer.selection) == 1 and type(Layer.selection[0]) == GSGuideLine:
                Layer.selection[0].name = self.w.box.editText.get()
                Glyphs.redraw()
            else:
                Message('Labeler', 'Select a guideline first :)', OKButton=None)
        except Exception as e:
            raise e

    def addGuideMetricsCallback(self, sender):
        try:
            metrics_dict = self.getDimensionsValues()
            for value in metrics_dict.items():
                self.addGuide(0, value[1], 0, value[0])
            self.addGuide(0, 0, 0, 'baseline')
            Glyphs.redraw()
        except Exception as e:
            raise e
            Glyphs.showMacroWindow()

    def deleteGlobalCallback(self, sender):
        font = Glyphs.font
        font_master = font.selectedFontMaster
        font_master.guides = []
        Glyphs.redraw()

    def deleteLocalCallback(self, sender):
        for layer in Glyphs.font.selectedLayers:
            glyph = layer.parent

        # delete guidelines:
        glyph.beginUndo()
        layer.guides = []
        glyph.endUndo()


LabelerWindow()
