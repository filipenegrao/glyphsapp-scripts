#MenuTitle: Export Sbix Color Font
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

from vanilla import *
from os.path import expanduser
from AppKit import NSOpenPanel
import subprocess



class ExportAllOPenFonts(object):

    def __init__(self):
        super(ExportAllOPenFonts, self).__init__()

        # default folder:
        home = expanduser("~")
        folder_path = home

        fonts_list = self.opened_fonts_display()

        # GUI sizes width and height
        w_window = 250
        h_window = 350

        # GUI
        self.w = Window((w_window, h_window), "Export all")
        self.w.label1 = TextBox((20, 20, -20, 20), "Export to", alignment = "center", sizeStyle = "small")
        self.w.path = TextBox((20, 45, -20, 40), folder_path, alignment = "center", selectable = "True", sizeStyle = "small")
        self.w.select_folder = Button((20, 105, -20, 20), "Change Folder", callback = self._file_dialog_callback)
        self.w.line = HorizontalLine((80, 163, -80, 1))
        self.w.list_fonts = TextBox((20, 190, -20, -20), fonts_list, alignment = "center", sizeStyle = "small")
        self.w.export_button = Button((20, -40, -20, 20), "Export", callback = self.py_magic)
        self.w.export_button.bind("\r", []) # shortcut \r = Return

        self.w.open()

    def opened_fonts_display(self):
        fonts_list = []

        for font in Glyphs.fonts:
            for instance in font.instances:
                fonts_list.append(instance.familyName + ' ' + instance.name)

        fonts_list =  '\n'.join(fonts_list)
        return fonts_list

    def _file_dialog_callback(self, message=None):
        try:
            panel = NSOpenPanel.openPanel()
            panel.setCanCreateDirectories_(True)
            panel.setCanChooseDirectories_(True)
            panel.setCanChooseFiles_(False)
            panel.setAllowsMultipleSelection_(False)
            
            if panel.runModal() == 1:
                for item in panel.URLs():
                    new_url = '/' + str(item).strip('file:/')
                    self.w.path.set(new_url)
                    print(new_url)
                    return new_url
            else:
                pass
        except Exception as e:
            raise e

    def sbix_exporter(self):
        # get the folder location
        folder_location = self.w.path.get()

        for font in Glyphs.fonts:
            for instance in font.instances:
                instance.generate('TTF', FontPath = folder_location, AutoHint = False, RemoveOverlap = False)

        Glyphs.showNotification('Export fonts', 'The export of %s was successful.' % (Glyphs.font.familyName))
        subprocess.Popen(["open", folder_location])

    def py_magic(self, sender):
        self.sbix_exporter()

ExportAllOPenFonts()