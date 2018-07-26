# MenuTitle: Open all comb marks in a new tab

__doc__ = """

Open related glyphs in a new tab.
E.g., if you select the tilde diacritic and run it,
it will open all the glyphs that have the string 'tilde' on it.

"""

font = Glyphs.font

for layer in Font.selectedLayers:
    glyph = layer.parent
    gname = glyph.name

selected_layer_name =  Font.selectedLayers[0].parent.name
tab_text = ""

for g in font.glyphs:
    if selected_layer_name in g.name:
        new_line = "/%s" % g.name
        tab_text += new_line

if tab_text:
    font.newTab(tab_text)
