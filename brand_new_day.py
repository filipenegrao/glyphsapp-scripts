# MenuTitle: Brand New Day
# -*- coding: utf-8 -*-

__doc__ = """

With an open glyphs' file, this script creates a new folder named the
current date (Y-M-D format) with all the same stuff you have inside
the current file's folder.
Then, the script closes the opened file and opens the new one.

This script is based on Hannes Famira's workflow,
who was type design instructors on Type@Cooper 2017.

"""

from datetime import datetime
import os
from distutils.dir_util import copy_tree
# import glob


font = Glyphs.font

# Current filepath
current_file_path = font.filepath
current_folder_path = os.path.dirname(current_file_path)
# print current_file_path

# one level down, relative to the current folder path
one_level_down = os.path.split(current_folder_path)[0]
# print one_level_down

# get the current file name to later open the new file
current_file_name = os.path.split(current_file_path)[1]
# print current_file_name

# date stuff
now = datetime.now()
today = '%d-%d-%d' % (now.year, now.month, now.day)
# print today

new_folder = one_level_down + '/' + today
# print new_folder

# create a folder with the today's date
if not os.path.exists(new_folder):
    os.makedirs(new_folder)
else:
    print '%s already exists.' % new_folder

# Check if the file already exists in the new folder
# In case you run the program 2 times, for example:
os.chdir(new_folder)
if os.path.isfile(current_file_name):
    Glyphs.clearLog()
    Glyphs.showMacroWindow()
    print "The file %s already exists in %s" % (current_file_name, new_folder)
    print "You are currently on %s" % current_file_path
else:
    LAST_SOURCE = current_folder_path
    TODAYS_SOURCE = new_folder

    # Copy all files of the Current file's folder to the new folder created
    copy_tree(LAST_SOURCE, TODAYS_SOURCE)

    Glyphs.showNotification("Copy Current Font", "The current font's folder was copied to %s" % TODAYS_SOURCE)
    font.close()

    new_glyphs_file_path = new_folder + '/' + current_file_name
    Glyphs.open(new_glyphs_file_path)

    Glyphs.clearLog()
    Glyphs.showMacroWindow()

    print "****************************************************"
    print "Have a nice day design cool stuff!"
    print "This new file was created today (%s)." % now
    print "Current file path: %s" % Glyphs.font.filepath
    print "Log file: %s" % Glyphs.font.filepath
    print "****************************************************"
