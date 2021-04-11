# MenuTitle: Start a new project
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import os
from datetime import datetime

__doc__ = """

If you have the same folder structure for every project, this script creates that structure in a breeze.
Just edit the FOLDERS list to change my default structure.

"""


# date stuff
NOW = datetime.now()
TODAY = '%d-%d-%d' % (NOW.year, NOW.month, NOW.day)

FONT = Glyphs.font
PATH = GetFolder(message="Choose where your project will be at:", allowsMultipleSelection = False)
DIR = "/" + FONT.familyName
FNAME = (FONT.filepath).split("/")[-1]
SOURCES = PATH + DIR + "/" + "sources/"
DIR_DATE = SOURCES + TODAY
FULL_PATH = DIR_DATE + "/" + FNAME

# edit this if you want a different folder structure
FOLDERS = [
    "critiques",
    "mockups",
    "proofs",
    "fonts",
    "sources",
    "research",
    "data",
    "sketches"
]

# don't bother putting stuff in alpahbetical order.
# this line will do the trick
SRT_FOLDERS = sorted(FOLDERS)

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

if not os.path.exists(PATH + DIR):
    os.makedirs(PATH + DIR)
    print(("%s was created in %s") % (DIR, PATH))
    for folder in FOLDERS:
        os.makedirs(PATH + DIR + "/" + folder)
else:
    print(("The %s folder already exists in %s.") % (DIR, PATH))

if not os.path.exists(DIR_DATE):
    os.makedirs(DIR_DATE)
else:
    print(" ")
    print("It's all done, mate. Do not complicate things. Look:")

if FONT.filepath == None:
    print("Please, save you file first.")
else:
    os.rename(FONT.filepath, FULL_PATH)

Glyphs.showMacroWindow()

print(" ")
print("=" * 50)
print(" ")

list_files(PATH + DIR)
