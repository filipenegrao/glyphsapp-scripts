#MenuTitle: Export all Open Fonts to UFO
# -*- coding: utf-8 -*-

__doc__="""

(GUI) This script export all open fonts' masters as UFO to a selected folder.
The default folder is configured to 'your/font/folder/path'.
Vanilla required.

"""

from vanilla import *
import os
from os.path import expanduser
from AppKit import NSOpenPanel
import subprocess

class ExportAllOPenFonts(object):

    def __init__(self):
        super(ExportAllOPenFonts, self).__init__()

        # default folder:

        font_path = font.filepath
        folder_path = os.path.dirname(font_path)

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
            for master in font.masters:
                fonts_list.append(font.familyName + ' ' + master.name)

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
                    return new_url
            else:
                pass
        except Exception as e:
            raise e

    def send_files(self):
        # get the folder location
        folder_location = self.w.path.get()

        ufo_exporter = Glyphs.objectWithClassName_("GlyphsFileFormatUFO")
        # fontpath = font.filepath
        # folderpath = os.path.dirname(fontpath)


        # send all open files to the folder_location
        try:
            if len(Glyphs.fonts) == 0:
                Glyphs.showNotification('Export all open fonts', 'At least one font should be opened.')
            else:
                for font in Glyphs.fonts:
                    for master in Glyphs.font.masters:
                #       instance_font = instance.interpolatedFont
                #       ufo_exporter.setFontMaster_(instance_font.masters[0])
                        folder = folder_location
                        ufo_filepath = os.path.join(folder, font.familyName + "-" + master.name + ".ufo")
                        dest = NSURL.fileURLWithPath_(ufo_filepath)
                        ufo_exporter.writeUfo_toURL_error_(master, dest, None)
                Glyphs.showNotification('Export all open fonts', 'The fonts were exported successfully!')
                subprocess.Popen(["open", folder_location])
        except Exception as e:
            raise e

    def py_magic(self, sender):
        self.send_files()

ExportAllOPenFonts()
