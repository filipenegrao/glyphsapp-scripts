from __future__ import print_function


class OvershootTests(object):
    """docstring for OvershootTests"""
    
    def __init__(self):
        super(OvershootTests, self).__init__()

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
