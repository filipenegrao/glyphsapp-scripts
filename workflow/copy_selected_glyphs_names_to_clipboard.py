# MenuTitle: Copy selected glyphs' names to Clipboard
# -*- coding: utf-8 -*-

__doc__ = """

Copy the currection selection's name to the clipboard.

"""

import subprocess

font = Glyphs.font
gnames = '\n'.join(glyph.name for glyph in font.selection)

def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data

def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()

setClipboardData(gnames)
