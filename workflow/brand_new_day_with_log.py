# MenuTitle: Brand New Day (with log file)
# -*- coding: utf-8 -*-

__doc__ = """

With an open glyphs' file, this script creates a new folder named the
current date (Y-M-D format) with all the same stuff you have insidethe current file's folder.
The difference between this script and the "Brand New Day" is that this one creates and writes a log file (.md).

This script is based on Hannes Famira's workflow, who was my type design instructors during Type@Cooper 2017.

"""

from datetime import datetime
import os
from distutils.dir_util import copy_tree


# =========== FONT INFO & STUFF

FONT = Glyphs.font
FONT_NAME = FONT.familyName


# =========== DATES

NOW = datetime.now()
TODAY = str(NOW.date())
CTIME = NOW.ctime()


# =========== PATHS

FONT_PATH = FONT.filepath
CURRENT_FOLDER = os.path.dirname(FONT_PATH)
ONE_DOWN = os.path.split(CURRENT_FOLDER)[0]

LOG_NAME = FONT_NAME.lower().replace(" ", "_")
LOG_FOLDER = ONE_DOWN + "/" + '-logs'
LOG_FILE_MD = LOG_FOLDER + "/" + LOG_NAME + ".md"
LOG_FILE_TXT = LOG_FOLDER + "/" + LOG_NAME + ".txt"
NEW_FOLDER_PATH = ONE_DOWN + "/" + TODAY
LAST_SOURCE = CURRENT_FOLDER
TODAYS_SOURCE = NEW_FOLDER_PATH
GLYPHS_FILENAME = os.path.split(FONT_PATH)[1]

NEW_FILE_PATH = NEW_FOLDER_PATH + "/" + GLYPHS_FILENAME


# =========== FORMATED STRINGS

HEADER = u"""

# %s's log file
* Created: %s

*This log file was createad by a cool robot developed by Filipe Negrao ([hello@filipenegrao.com](mailto:hello@filipenegrao.com)).
If you have any complaints, please send a message to the cool robot. Otherwise, Filipe is available :).*

"""


# =========== FUNCTIONS

def check_path(path):
    path_exists = False
    if os.path.exists(path):
        path_exists = True
    return path_exists


def create_folder(folderpath):
    try:
        os.makedirs(folderpath)
    except Exception as e:
        raise e


def log_entry(last_mod_file_date):
    date_glyphs = {}
    date_glyphs[last_mod_file_date] = []
    for glyph in FONT.glyphs:
        if glyph.lastChange is not None:
            if glyph.lastChange.date() == last_mod_file_date:
                date_glyphs[last_mod_file_date].append(glyph.name)
    return date_glyphs


def dict_to_md_tag(d):
    for k in d:
        d[k] = ', '.join(map(str, d[k]))
    return "## %s\n**File path:** [%s](%s)\n \n **Glyphs changed:** %s \n" % (k, FONT_PATH, FONT_PATH, d[k])


def check_log_entry(filepath, str_line):
    has_txt = False
    with open(filepath, 'r') as fh:
        line = fh.readlines()
        for l in line:
            if str(str_line) not in l:
                pass
            else:
                has_txt = True
        return has_txt


def create_file(filepath, header_content=None):
    try:
        with open(filepath, 'w') as fh:
            fh.write(header_content)
    except Exception as e:
        raise e


def write_log(filepath, entry):
    try:
        with open(filepath, 'a') as fh:
            fh.write(entry)
            fh.close()
    except Exception as e:
        raise e


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


# =========== file handle's

LAST_MODIFIED = modification_date(FONT_PATH).date()

# duplicate folder with new date:
if not check_path(NEW_FOLDER_PATH):
    create_folder(NEW_FOLDER_PATH)
    copy_tree(LAST_SOURCE, TODAYS_SOURCE)

# create log folder if doesn't exists:
if not check_path(LOG_FOLDER):
    create_folder(LOG_FOLDER)

# create log files inside the new folder:
# this will only run if no previous log file exists
if not check_path(LOG_FILE_MD):
    create_file(LOG_FILE_MD, HEADER % (FONT_NAME, CTIME))
    create_file(LOG_FILE_TXT, HEADER % (FONT_NAME, CTIME))

# check if the data you wanna write is already there
if not check_log_entry(LOG_FILE_MD, LAST_MODIFIED):
    new_entry = log_entry(LAST_MODIFIED)
    str_entry = dict_to_md_tag(new_entry)
    write_log(LOG_FILE_MD, str_entry)
    write_log(LOG_FILE_TXT, str_entry)


# =========== notifications, open, close

Glyphs.showNotification("Copy Current Font", "The current font's folder was copied to %s" % TODAYS_SOURCE)
FONT.close()
Glyphs.open(NEW_FILE_PATH)
Glyphs.showMacroWindow()


print "****************************************************"
print "Have a nice day!"
print "This new file was created today (%s)." % TODAY
print "Current file path: %s" % Glyphs.font.filepath
print "Log file: %s" % LOG_FILE_MD
print "****************************************************"
