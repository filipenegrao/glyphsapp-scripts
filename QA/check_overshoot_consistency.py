font = Glyphs.font
Glyphs.clearLog()


above_lc = {
'round': ['a', 'b', 'c', 'd', 'e', 'g', 'h', 'm', 'n', 'o', 'p', 'q', 'r', 's']
}

bellow_lc = {
'round': ['a', 'b', 'c', 'd', 'e', 'g', 'o', 'p', 'q', 's', 't', 'u'],  # i, l
}

above_uc = {
}

bellow_uc = {
}

def overshoot_consistency(list_of_glyphs, reference_overshoot_value, tolerance):
    has_error = False
    for i, master in enumerate(font.masters):
        for glyph in font.glyphs:
            if glyph.name in list_of_glyphs:
                for layer in glyph.layers:
                    for path in layer.paths:
                        for node in path.nodes:
                            if node.y > (reference_overshoot_value - tolerance) and node.y < (reference_overshoot_value + tolerance):
                                if node.type != "offcurve" and node.y != reference_overshoot_value:
                                    print("## Font Family: %s | Master: %s | Overshoot reference: %s \n"  % (font.familyName, master.name, str(reference_overshoot_value)))
                                    print("* '%s' -> node.y are at '%s' \n" % (glyph.name, node.y))
                                    has_error = True
    return has_error


for i, master in enumerate(font.masters):
    xheight = master.xHeight
    o = font.glyphs['o']
    round_l = above_lc['round']
    overshoot = o.layers[i].bounds.origin.y
    ovt_above = xheight + (-overshoot)
    has_error = overshoot_consistency(round_l, ovt_above, 15)


if has_error:
    # create log folder if doesn't exists:
    if not check_path(REPORT_FOLDER):
        create_folder(REPORT_FOLDER)

    # create a new file with the reporter:
    if not check_path(REPORT_FILE_TXT):
        create_file(REPORT_FILE_TXT, HEADER % (font.familyName, TODAY))

