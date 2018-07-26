# MenuTitle: Add kerning groups for dlig glyphs
# encoding: utf-8
# Copyright: Filipe Negrão, 2018.


__doc__="""

This script uses Georg's 'Set Kerning Group' as a base and depends on its code. 
"""

# For this script to work, it depends on exporting set_kerning_groups.
# This means that the set_kerning_groups.py needs to be in the same folder as this script.
from set_kerning_groups import *

font = Glyphs.font

# brings macro window to front and clears its log:
Glyphs.clearLog()
Glyphs.showMacroWindow()

for g in Font.selectedLayers:
    glyph = layer.parent

    # If the selected glyphs is a ligature and it has .dlig in it's name
    if glyph.subCategory == "Ligature" and '.dlig' in glyph.name:
        gname = g.name

        # split dlig names into a list of its components, e.g.: L_E.dlig will return ['L', 'E']
        processed_name = gname.strip('.dlig').split('_')

        left_key = processed_name[0]  # get the first item of the list
        right_key = processed_name[-1]  # get the last item of the list, especially because some ligatures might be made of more than two glyphs.  

        # check if the selected glyph has a correspondent in DefaultKeys (that is inside set_kerning-group.py)
        if left_key in DefaultKeys and right_key in DefaultKeys:

            # creates a new list with the first and the last values
            # so, for example, T_H_Eacute.dlig will have a list that is equivalent to
            # the kerning group of the 'T' (for the left side) and the 'Eacute' for the right side.
            new_values = [left_key, right_key]  

            # Then, the new values (left and right) has to be added to the dictionary
            # e.g. DefaultKeys['E_Agrave.dlig'] = ['H', 'A'] 
            DefaultKeys[gname] = new_values
            print "Added: \"%s\" : [\"%s\", \"%s\"]," % (gname, new_values[1], new_values[0])


# calls the main() function from Georg's 'Set Kerning Group'
main()
