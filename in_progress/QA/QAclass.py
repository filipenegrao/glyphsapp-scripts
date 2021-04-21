from __future__ import print_function
import os


class QAclass(object):
    """docstring for QAclass"""

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
            self.report("# QA report of untitled family = NOTHING TO DO\n", init=True)
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
