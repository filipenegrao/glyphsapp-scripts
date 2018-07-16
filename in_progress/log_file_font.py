#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import json
from datetime import datetime


FONT = Glyphs.font
FONTPATH = FONT.filepath

NOW = datetime.now()
TODAY = '%d-%d-%d' % (NOW.year, NOW.month, NOW.day)

CURRENTFOLDER = os.path.dirname(FONTPATH)
ONELEVELDOWN = os.path.split(CURRENTFOLDER)[0]

LOGNAME = FONT.familyName.lower().replace(" ", "_")
LOGFILE = ONELEVELDOWN + '/' + LOGNAME + '_log.txt'


def check_file(filepath):
    '''
    If the filepath does not exists, create.
    return -> filepath = current/folder/filename.txt
    '''
    try: 
        file = open(filepath, 'r')
    except IOError:
        file = open(filepath, 'w')
        json.dump([], file)
    return filepath


def check_content(filepath, some_content):
    with open(filepath, 'r') as fh:
        # remove /n from strings
        content_list = [x.strip() for x in fh.readlines()]
        for item in content_list:
            if some_content not in item.split():
                continue
            else:
                return True


def compare_two_lists(l1, l2):
    diff = set(l1).symmetric_difference(set(l2))
    return diff


def add_2_json(filepath, new_entry):

        with open(filepath) as feedsjson:
            feeds = [json.load(feedsjson)]
        feeds.append(new_entry)
        
        with open(filepath, mode='w') as f:
            f.write(json.dumps(feeds, indent=4))


def masters_glyphs():
    masters_dict = {}
    for i, master in enumerate(FONT.masters):
        mname = master.name
        masters_dict[mname] = []   
        for glyph in FONT.glyphs:    
            id_master = glyph.layers[FONT.masters[i].id]
            if len(id_master.paths) != 0:
                masters_dict[mname].append(glyph.name)
    return masters_dict

todays_glyphs = masters_glyphs()
todays_entry = (TODAY, todays_glyphs)


def main():
    fp = check_file(LOGFILE)
    if not check_content(fp, TODAY):
        add_2_json(fp, todays_entry)

main()


# ----------- testing

import os
cwd = os.getcwd()
f = cwd + '/new_file002.txt'

print f  # def check_file
# print check_content(f, 'ops')  # def check_content

new_file = check_file(f)
new_data = {'123': ['a', 'b', 'c', 'd'], '456': ['a', 'b', 'c', 'd', 'e', 'f', 'g']}

add_2_json(new_file, new_data)

l1 = new_data['123']
l2 = new_data['456']

list3 = ['a', 'b', 'c', 'd']
list4 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

print compare_two_lists(list3, list4)
