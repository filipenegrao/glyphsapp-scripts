# MenuTitle: Change Ascenders & Descenders
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import GlyphsApp
from vanilla import *

__doc__ = """

(GUI) This code changes the height of ascenders or descenders of selected glyphs in Edit View.
Vanilla required.

**Pro tip:** Use Arrows Up and Down as shortcuts.

"""


font = Glyphs.font

class AscenderDescenderModifier(object):

    def __init__(self):
        super(AscenderDescenderModifier, self).__init__()

        self.w = Window((280, 230), "Game Changer")
        self.w.tabs = Tabs((10, 10, -10, -10), ["Ascender", "Descender"])

        # tab 1
        ascender_tab = self.w.tabs[0]
        ascender_tab.txt_overshoot = TextBox((20, 30, -20, 20), "Overshoot")
        ascender_tab.overshoot = EditText((120, 30, -20, 20), "15")
        ascender_tab.txt_amount = TextBox((20, 60, -20, 20), "Raise Amount")
        ascender_tab.amount = EditText((120, 60, -20, 20), "10")

        ascender_tab.label_shortcut = TextBox((30, 98, -20, 20), "You can use the keyboard's arrows :)", sizeStyle = "small")
        ascender_tab.button_up = Button((20, 120, -20, 20), "Up", callback=self.move_stuff_ascender)
        ascender_tab.button_up.bind("uparrow", []) # shortcut
        ascender_tab.button_down = Button((20, 150, -20, 20), "Down", callback=self.move_stuff_ascender)
        ascender_tab.button_down.bind("downarrow", []) # shortcut

        # tab 2
        descender_tab = self.w.tabs[1]
        descender_tab.txt_overshoot = TextBox((20, 30, -20, 20), "Overshoot")
        descender_tab.overshoot = EditText((120, 30, -20, 20), "15")
        descender_tab.txt_amount = TextBox((20, 60, -20, 20), "Raise Amount")
        descender_tab.amount = EditText((120, 60, -20, 20), "10")
        descender_tab.button_up = Button((20, 120, -20, 20), "Up", callback=self.move_stuff_descender)
        descender_tab.button_up.bind("uparrow", []) # shortcut
        descender_tab.button_down = Button((20, 150, -20, 20), "Down", callback=self.move_stuff_descender)
        descender_tab.button_down.bind("downarrow", []) # shortcut

        self.w.open()

    def up_ascender(self):
        overshoot = float(self.w.tabs[0].overshoot.get())
        raise_amount = float(self.w.tabs[0].amount.get())
        x_height = font.selectedFontMaster.xHeight

        for layer in Font.selectedLayers:
            glyph = layer.parent
            glyph.beginUndo()
            for path in layer.paths:
                for node in path.nodes:
                    if node.y > x_height + overshoot:
                        node.y += raise_amount
                    else:
                        pass
            glyph.endUndo()

    def down_ascender(self):
        overshoot = float(self.w.tabs[0].overshoot.get())
        raise_amount = float(self.w.tabs[0].amount.get())
        x_height = font.selectedFontMaster.xHeight

        for layer in Font.selectedLayers:
            glyph = layer.parent
            glyph.beginUndo()
            for path in layer.paths:
                for node in path.nodes:
                    if node.y > x_height + overshoot:
                        node.y -= raise_amount
                    else:
                        pass
            glyph.endUndo()

    def up_descender(self):
        overshoot = -float(self.w.tabs[1].overshoot.get())
        raise_amount = -float(self.w.tabs[1].amount.get())
        baseline = 0.0

        for layer in Font.selectedLayers:
            glyph = layer.parent
            glyph.beginUndo()
            for path in layer.paths:
                for node in path.nodes:
                    if node.y < baseline + overshoot:
                        node.y -= raise_amount
                    else:
                        pass
            glyph.endUndo()

    def down_descender(self):
        overshoot = -float(self.w.tabs[1].overshoot.get())
        raise_amount = -float(self.w.tabs[1].amount.get())
        baseline = 0.0

        for layer in Font.selectedLayers:
            glyph = layer.parent
            glyph.beginUndo()
            for path in layer.paths:
                for node in path.nodes:
                    if node.y < baseline + overshoot:
                        node.y += raise_amount
                    else:
                        pass
            glyph.endUndo()

    def move_stuff_ascender(self, sender):
        try:
            # Button up
            if sender is self.w.tabs[0].button_up:
                self.up_ascender()
                Glyphs.redraw()

            # Button down
            elif sender is self.w.tabs[0].button_down:
                self.down_ascender()
                Glyphs.redraw()
            else:
                pass
        except Exception as e:
            raise e

    def move_stuff_descender(self, sender):
        try:
            # Button up
            if sender is self.w.tabs[1].button_up:
                self.up_descender()
                Glyphs.redraw()

            # Button down
            elif sender is self.w.tabs[1].button_down:
                self.down_descender()
                Glyphs.redraw()

            else:
                pass
        except Exception as e:
            raise e


AscenderDescenderModifier()
