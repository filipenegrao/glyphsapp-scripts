# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from datetime import datetime


FONT = Glyphs.font
FONTPATH = FONT.filepath

NOW = datetime.now()
TODAY = '%d-%d-%d' % (NOW.year, NOW.month, NOW.day)

CURRENTFOLDER = os.path.dirname(FONTPATH) 
ONELEVELDOWN = os.path.split(CURRENTFOLDER)[0]

LOGNAME = FONT.familyName.lower().replace(" ", "_") + '_log.md' 
LOGFOLDER = ONELEVELDOWN + "/" + '-logs'
LOGFILE = LOGFOLDER + "/" + LOGNAME


HEADER = u"""

# %s's log file
* Created: %s 

*This log file was createad by a cool robot developed by Filipe Negrao ([hello@filipenegrao.com](mailto:hello@filipenegrao.com)).
If you have any complaints, please send a message to the cool robot. Otherwise, Filipe is available :).*

"""



ENTRIES = u"""## %s

* file path: [%s](%s)

Modified Glyphs: 

%s

"""


def check_folder(folderpath):
    '''
    If the folder does not exists, create.
    return -> folderpath = current/folder/log_file/
    '''
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        print('The log file was created in %s' % folderpath)
    else:
        print('%s already exists.' % folderpath)
    return folderpath


def check_file(filepath):
    '''
    If the filepath does not exists, create.
    return -> filepath = current/folder/filename.txt
    '''
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        print('The log file was created in %s' % filepath)
    else:
        pass
        print('Log file already exists in %s.' % filepath)
    return filepath


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


def simple_log_entry(last_mod_file):
    mod_glyphs = u""
    for glyph in FONT.glyphs:
        if glyph.lastChange.date() == last_mod_file:
            mod_glyphs += glyph.name + ', '
    mod_glyphs = mod_glyphs[:-1-1]  # remove the last comma
    return mod_glyphs
    

def write_log(filepath, header, entry):
    if os.path.getsize(filepath) == 0:
        with open(filepath, 'a') as fh:
            fh.write(header)
            fh.write(entry)
    else:
        with open(filepath, 'a') as fh:
            fh.write(entry)

    fh.close()


def check_log_entry(filepath, date):
    has_date = False
    with open(file_path, 'r') as fh:
        line = fh.readlines()
        for l in line:
            if str(date) not in l:
                pass
            else:
                has_date = True
        return has_date


# ==== MAGIC ====

last_mod_date = modification_date(FONTPATH).date()
folder_path = check_folder(LOGFOLDER)
file_path = check_file(LOGFILE)
new_data = simple_log_entry(last_mod_date)
new_header = HEADER % (FONT.familyName, TODAY)
new_entry = ENTRIES % (last_mod_date, FONTPATH, FONTPATH, new_data)

if not check_log_entry(file_path, last_mod_date):
    write_log(file_path, new_header, new_entry)
