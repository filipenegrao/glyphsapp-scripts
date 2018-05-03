from datetime import datetime
import os
import json

font = Glyphs.font

# Current filepath
current_file_path = font.filepath
current_folder_path = os.path.dirname(current_file_path)
one_level_down = os.path.split(current_folder_path)[0]

FNAME = font.familyName
GLYPHS_FILE = one_level_down + '/' + '%s_glyphs.txt' % FNAME.lower().replace(" ", "_")

FONT_MASTERS = {}
GLYPHS_ADDED = []
GLYPHS_CHANGED = []

NOW = datetime.now()
TODAY = '%d-%d-%d' % (NOW.year, NOW.month, NOW.day)

if not GLYPHS_FILE:
    for i, master in enumerate(font.masters):   
        current_master = master.name

        FONT_MASTERS[current_master] = []
        num_of_glyphs = 0

        for glyph in font.glyphs:
            id_master = glyph.layers[font.masters[i].id]

            if len(id_master.paths) != 0:
                num_of_glyphs += 1

                FONT_MASTERS[current_master].append(glyph.name)

    with open(GLYPHS_FILE, 'w+') as fh:
        json.dump(FONT_MASTERS, fh, indent=4, separators=(',', ': '))

with open(GLYPHS_FILE) as fh:
    data = json.load(fh)


for i, master in enumerate(font.masters):   
    current_master = master.name

    for glyph in font.glyphs:
        id_master = glyph.layers[font.masters[i].id]

        if len(id_master.paths) == 0:
            continue
        else:
            if glyph.name not in data[current_master]:
                print 'Glyph added in %s: %s' % (current_master, glyph.name)


