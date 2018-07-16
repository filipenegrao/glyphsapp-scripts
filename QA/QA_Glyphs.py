import os
# import sys


CREATE_ERRORS = False

DIACRITICS = (
    'circumflex', 'tilde', 'macron', 'breve', 'dotaccent', 'ring',
    'cedilla', 'hungarumlaut', 'ogonek', 'caron'
)

SYMMETRIC_GLYHPS = (
    'exclam', 'o', 'v', 'w', 'A', 'O', 'V', 'H', 'I', 'W', 'T', 'hyphen',
    'endash', 'emdahs', 'brokenbar', 'plus', 'bar')  # 'S', 'X', 'Y', 'Z', 'U'?

SIDE_LEFT_GROUPS = {
    'n': ('n', 'm', 'encyrillic'),  # 'b'?
    'h': ('b', 'k'),
    'o': ('c', 'd', 'q', 'o', 'oe'),
    'H': ('B', 'D', 'E', 'F', 'H', 'I', 'K', 'L', 'P', 'R'),  # 'M', 'N'?
    'O': ('C', 'G', 'O', 'Q'),
    'bar': ('bar', 'brokenbar'),
    'period': ('period', 'ellipsis'),
}

SIDE_RIGHT_GROUPS = {
    'o': ('o', 'p', 'b', 'thorn'),
    'e': ('e', 'oe'),
    'n': ('n', 'h', 'm'),  # 'b'?
    'H': ('H', 'I'),  # 'M', 'N'?
    'E': ('E', 'AE', 'OE'),
    'O': ('D', 'O', 'Q'),
    'bar': ('bar', 'brokenbar'),
    'period': ('period', 'ellipsis')
}

CROSS_GROUPS = (
    ('parentleft', 'parenright'),
    ('bracketleft', 'bracketright'))

# OVERSHOOTS
TOLERANCE = 10
OVERSHOOT = 14

# Overshoot Groups:
OVERSHOOT_UC_ABOVE = {
    'round': ('O', 'C', 'Q', 'G', 'S'),
    'diagonals': ('A')
}

OVERSHOOT_UC_BELLOW = {
    'round': ('O', 'C', 'G', 'S'),
    'diagonals': ('V', 'W')
}

OVERSHOOT_LC_ABOVE = {
    'round': ('a', 'b', 'c', 'd', 'e', 'g', 'h', 'm', 'n', 'o', 'p', 'q', 'r', 's')
}

OVERSHOOT_LC_BELLOW = {
    'round': ('a', 'b', 'c', 'd', 'e', 'g', 'o', 'p', 'q', 's', 't', 'u'),  # i, l, t
    'diagonals': ('v', 'w')
}


class QADemo(object):

    # added a half tabular width for half tab punctuation
    def __init__(self, fonts, tnum=None, hashalftab=False):
        self.fonts = fonts
        self.tnum = tnum
        self.hashalftab = hashalftab

        if fonts:
            # stores the file name in the root as the Glyphs file
            rootPath = '/'.join(fonts[0].filepath.split('/')[:-1])
            self.report_path = rootPath + '/QA-Report-%s.txt' % fonts[0].familyName 
            self.report('## QA report of family %s\n' % fonts[0].familyName, init=True)
            self.openReport()
        else:
            rootPath = os.filepath.expanduser('~/Desktop')
            self.report_path = rootPath + '/QADemo-Report-Untitled.txt'
            self.report('## QADemo report of untitled family = NOTHING TO DO\n', init=True)
            self.openReport()
        print('Report file is here:  "%s"' % self.report_path)

    def __len__(self):
        return len(self.fonts)

    def openReport(self):
        os.system('open "%s"' % self.report_path)

    def report(self, s, init=False):
        if init:
            report_file = open(self.report_path, 'w')
        else:
            report_file = open(self.report_path, 'a')
        report_file.write(s)
        report_file.close()

    def test(self):
        """
        This method test separate fonts of self.fonts and their relations.

        - Per font
        - yourPersonalTest
        - testGroupsConsistencies
        - testKerningConsistencies
        - featuresAndGroups
        - testAnchors (positions, naming)
        - contourDirections
        - componentConsistency
        - overlappingOnCurvePoint
        - breakingTangents
        - testOpenContours
        - testMetrics
        (Test ascender, descender, xHeight and compare with font.info metrics)
        - Per family
        - glyphSet
        - testInterpolationCompatibilty
        (numberContours, order, amountOfPoints, typeOfPoints, components, inflection)
        - testDesignSpace (masters, axes)
        - infoCheck (font.info, OS/2, metric, etc.)
        """
        has_error = False        


        if CREATE_ERRORS:
            self.createErrors()
        has_error |= self.testWidths()  # (negative width, group of sidebearings)
        has_error |= self.testSymmetry()  # Test symmetric sides
        has_error |= self.testSidebearingGroups()  # Testing the sides of groups of glyphs
        has_error |= self.italicCheck()  # Check if italic fits name and angle
        has_error |= self.yourPersonalTest()  # This could be your personal customized test
        has_error |= self.sidebearingAlmostSame()  # Check if difference between sidebearrings are dangerously close
        has_error |= self.glyphNotOnBaseline()
        has_error |= self.hasAlmostStraightLine()
        has_error |= self.checkOvershoot()  # Check overshoot consistency

        if not has_error:
            print('All ok')
        else:
            print('Work to do!')

    def createErrors(self):
        # Create some artifical errors in the fonts to test the functions.
        for font in fonts:
            font.glyphs['A'].layers[0].width = -10
            if 'gravecomb' in font.glyphs.keys():
                font.glyphs['gravecomb'].layers[0].width = 2
            if self.tnum is not None and 'five.tnum' in font.glyphs.keys():
                font.glyphs['five.tnum'].layers[0].width = self.tnum + 2

    def testWidths(self):
        u"""Test on negative widths for all glyphs in all fonts.
        Test on non-zero width for glyphs that have a name ending with "cmb"
        """
        has_error = False
        for font in self.fonts:
            # Test if there is a negative width
            for g in font.glyphs:
                # Width checking
                if g.layers[0].width < 0:
                    self.report('# %s Negative width for "%s:%d"\n' % (font.filepath.split('/')[-1], g.name, g.layers[0].width))
                    has_error = True
                elif "comb" in g.name and g.layers[0].width != 0:
                    self.report('# %s Non-zero width for "%s:%d"\n' % (font.filepath.split('/')[-1], g.name, g.layers[0].width))
                    has_error = True
                elif g.name in DIACRITICS and g.layers[0].width != 0:
                    self.report('# %s Non-zero width for "%s:%d"\n' % (font.filepath.split('/')[-1], g.name, g.layers[0].width))
                    has_error = True
                elif self.tnum is not None and g.name.endswith('.tnum') and g.layers[0].width != self.tnum: #ADDED new line for half tabular punctuation is this okay?
                    if g.layers[0].width == self.tnum/2 and self.hashalftab:
                            self.report('# %s FYI %s is on half tabular width which is %d\n' % (font.filepath.split('/')[-1], g.name, self.tnum/2))
                    else:
                        self.report('# %s Wrong tab width for "%s:%d" instead %d\n' % (font.filepath.split('/')[-1], g.name, g.layers[0].width, self.tnum, ))
                        has_error = True
        return has_error

    def testSymmetry(self):

        """Test all glyphs in all fonts. If they fit the name of being a symmetric glyph,
        then test if the g.leftMargin == g.rightMargin.
        For italics test g.angledLeftMargin == g.angledRightMargin.
        """
        for font in self.fonts:
            fontFile = font.filepath.split('/')[-1]
            if 'Italic' in fontFile or 'Italic' in font.masters[0].name or font.masters[0].italicAngle == 0: #one of these will be italic. 
                has_error = False
                for g in font.glyphs:
                    if g.name in SYMMETRIC_GLYHPS and g.layers[0].LSB != g.layers[0].RSB:
                        self.report('# %s Glyph "%s" sidebearing (%d,%d) are not symmetric\n' % (font.filepath.split('/')[-1], g.name, g.layers[0].LSB, g.layers[0].RSB))
                        has_error = True
                    return has_error
            else:
                has_error = False
                for g in font:
                    if g.name in SYMMETRIC_GLYHPS and g.layers[0].LSB != g.RSB:
                        self.report('# %s Glyph "%s" sidebearing (%d,%d) are not symmetric\n' % (font.filepath.split('/')[-1], g.name, g.layers[0].LSB, g.layers[0].RSB))
                        has_error = True
        return has_error

    def testSidebearingGroups(self):
        """
        Test all glyphs in all fonts if they have the same
        sidebearing as the other in the group.

        """

        has_error = False
        for font in self.fonts:
            for baseGlyphName, group in SIDE_LEFT_GROUPS.items():
                if baseGlyphName not in font.glyphs:
                    continue
                for gname in group:
                    if gname not in font.glyphs:
                        continue
                    blsb = font.glyphs[baseGlyphName].layers[0].LSB
                    lsb = font.glyphs[gname].layers[0].LSB
                    if blsb != lsb:
                        self.report('# %s Glyph "%s:%d" left sidebearing is not same as "%s:%d"\n' % (font.filepath.split('/')[-1], baseGlyphName, blsb, gname, lsb))
                        has_error = True
            for baseGlyphName, group in SIDE_RIGHT_GROUPS.items():
                if baseGlyphName not in font.glyphs:
                    continue
                for gname in group:
                    if gname not in font.glyphs:
                        continue
                    brsb = font.glyphs[baseGlyphName].layers[0].RSB
                    rsb = font.glyphs[gname].layers[0].RSB
                    if brsb != rsb:
                        self.report('# %s Glyph "%s:%d" right sidebearing is not same as "%s:%d"\n' % (font.filepath.split('/')[-1], baseGlyphName, brsb, gname, rsb))
                        has_error = True
        return has_error

    def italicCheck(self):
        has_error = False
        for font in self.fonts:
            fontFile = font.filepath.split('/')[-1]
            if 'Italic' in fontFile and not 'Italic' in font.masters[0].name:
                self.report('# Font file name "%s" contains "Italic" and font.info.styleName "%s" does not\n' % (fontFile, font.info.styleName))
                has_error = True
            if not 'Italic' in fontFile and 'Italic' in font.masters[0].name:
                self.report('# font.info.styleName "%s" contains "Italic" and font file name "%s" does not\n' % (font.info.styleName, fontFile))
                has_error = True
            if 'Italic' in fontFile and font.masters[0].italicAngle == 0:
                self.report('# font "%s" is italic, but font.info.italicAngle is 0' % fontFile)
                has_error = True
            if not 'Italic' in fontFile and font.masters[0].italicAngle != 0:
                self.report('# font "%s" is not italic, but font.info.italicAngle is non 0' % fontFile)
                has_error = True
        return has_error

    def sidebearingAlmostSame(self):
        has_error = False
        for font in self.fonts:
            for g in font.glyphs:
                if 0 < abs(g.layers[0].LSB - g.layers[0].RSB) < 2:
                    self.report('# %s Glyph "%s" is almost symmetric but not \n' % (font.filepath.split('/')[-1], g.name))
                    has_error = True
        return has_error


    def glyphNotOnBaseline(self):
        has_error = False
        for font in self.fonts:
            for g in font.glyphs:
                for n in g.layers[0].paths:
                    for p in n.nodes:
                        if -2 <= p.y <= 2 and not p.y == 0:
                            self.report('# %s Glyph "%s" seems to be off baseline by %d points \n' % (font.filepath.split('/')[-1], g.name, p.y))
                            break #If the character has a straight path then it has repeating y values.
        return has_error

    def hasAlmostStraightLine(self):
        """
        Check if 1 pt difference bettween consecutive points,
        which indicates an almost straight line (but not really).

        """
        has_error = False
        for font in self.fonts:
            for g in font.glyphs:
                for n in g.layers[0].paths:
                    consecutiveX = []
                    consecutiveY = []
                    for p in n.nodes:
                        if len(consecutiveX) < 2:
                            consecutiveX.append(p.x)
                            consecutiveY.append(p.y)
                        else:
                            del consecutiveX[0]
                            del consecutiveY[0]
                            consecutiveX.append(p.x)
                            consecutiveY.append(p.y)
                        if len(consecutiveX) == 2:
                            if 0 < abs(consecutiveX[0]-consecutiveX[1]) <= 2 and consecutiveY[0]-consecutiveY[1] != 0:
                                self.report("# %s glyph %s; Vertical Segment Not Straight at (%s,%s) with values %s \n" % (font.filepath.split('/')[-1], g.name, p.x, p.y, consecutiveX))
                            if 0 < abs(consecutiveY[0]-consecutiveY[1]) <= 2 and consecutiveX[0]-consecutiveX[1] != 0:
                                self.report("# %s glyph %s; Horizontal Segment Not Straight at (%s,%s) with values %s \n" % (font.filepath.split('/')[-1], g.name, p.x, p.y, consecutiveY))
        return has_error

    def checkOvershoot(self):

    """
    The idea of this test is to check the overshoot consistency between glyphs.
    For that, it takes a value as argument and check if the glyph has an anchor
    with the same value. If not, it should return hasError = True.

    """

    hasError = False

    for font in self.fonts:

        capAbove = font.info.capHeight + OVERSHOOT
        xAbove = font.info.xHeight + OVERSHOOT
        baseBelow = OVERSHOOT

        print capAbove, xAbove, baseBelow

        for g in font:
            if g.name in OVERSHOOT_UC_ABOVE.get("round"):
                errorPoints = []
                for contour in g:
                    for p in contour.bPoints: # You only want to test if the y is in range of the cap height.
                        if p.anchor[1] < (capAbove - TOLERANCE) or p.anchor[1] > (capAbove + TOLERANCE):
                            continue # Not interested in points that are outside the range
                        if p.anchor[1] != capAbove: # Now this one has to match the overshoot value.
                            errorPoints.append(p.anchor)
                if errorPoints:
                    self.report('# %s Glyph "%s" has points "%s" error in overshoot \n' % (font.path.split('/')[-1], g.name, errorPoints))
                    hasError = True
    return hasError

    def yourPersonalTest(self):
        has_error = False
        # ... You test code here
        return has_error

# -------------------------------------------

fonts = Glyphs.fonts
qa_r2d2 = QADemo(fonts, tnum=None, hashalftab=False) 
qa_r2d2.test()
print(len(qa_r2d2)) # More sunstainable
