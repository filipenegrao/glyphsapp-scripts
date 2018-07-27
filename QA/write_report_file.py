from datetime import datetime
import os
from distutils.dir_util import copy_tree


# =========== DATES

NOW = datetime.now()
TODAY = str(NOW.date())
CTIME = NOW.ctime()

# =========== PATHS

FONT_PATH = FONT.filepath
CURRENT_FOLDER = os.path.dirname(FONT_PATH)
ONE_DOWN = os.path.split(CURRENT_FOLDER)[0]

REPORT_NAME = FONT_NAME.lower().replace(" ", "_")
REPORT_FOLDER = ONE_DOWN + "/" + '-QA_reporter'
REPORT_FILE_TXT = REPORT_FOLDER + "/" + REPORT_NAME + CTIME + ".txt"
GLYPHS_FILENAME = os.path.split(FONT_PATH)[1]

NEW_FILE_PATH = NEW_FOLDER_PATH + "/" + GLYPHS_FILENAME

HEADER = u"""

# %s's report file
* Created: %s

"""


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


def create_file(filepath, header_content=None):
    try:
        with open(filepath, 'w') as fh:
            fh.write(header_content)
    except Exception as e:
        raise e


def write_report(filepath, entry):
    try:
        with open(filepath, 'a') as fh:
            fh.write(entry)
            fh.close()
    except Exception as e:
        raise e


def report(s, init=False):
    if init:
        report_file = open(report_path, 'w')
    else:
        report_file = open(report_path, 'a')
    report_file.write(s)
    report_file.close()


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

