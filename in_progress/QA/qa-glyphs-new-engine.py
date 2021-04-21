# MenuTitle: [ *** TESTER *** ]
# -*- coding: utf-8 -*-

__doc__="""


"""

import os


class QAEngine(object):
	"""docstring for QAEngine"""
	
	
	def __init__(self, font, tab=None):
		super(QAEngine, self).__init__()
		self.font = font
		self.tab = tab
		self.report_path = self.md_path()

		if not os.path.isfile(self.report_path):
			self.report_header()
	
	def __len__(self):
		return len(self.font.masters)

	def num_masters(self):
		return len(self.font.masters)

	def num_instances(self):
		return len(self.font.instances)

	def md_path(self):
		root_path = '/'.join(self.font.filepath.split('/')[:-1])
		file_name = "".join(self.font.familyName.split()) # remove whitespace
		report_path = root_path + '/QAEngine-Report-{}.md'.format(file_name)
		return report_path

	def check_md_path(self, path):
		return os.path.isfile(path)

	def report(self, s, init=False): 
		if init:
			with open(self.report_path, 'w') as report_file:
				report_file.write(s)
		else:
			with open(self.report_path, 'a') as report_file:
				report_file.write(s)

	def header_data(self, info):
		return {
		'GLYPHS_VERSION': Glyphs.versionNumber,
		'FONT_NAME': self.font.familyName,
		'FONT_PATH': self.font.filepath,
		'UPM': self.font.upm,
		'FONT_VERSION': '{}.{}'.format(self.font.versionMajor, self.font.versionMinor),
		'CREATION_DATE': self.font.date,
		'DESIGNER': self.font.designer,
		'NUM_MASTERS': len(self.font.masters),
		'MASTERS': [master.name for master in self.font.masters],
		'MASTERS_IDS': [self.font.masters[i].id for i in range(self.num_masters())]
		}[info]

	def header_doc(self):
		return ('# {} — QA Report\n'
		"* **Designer** {}\n"
		'* **File Location** [{}]({})\n'
		'* **UPM** {}\n'
		'* **Glyphs App Version** {}\n'
		'* **Date of Creation** {}\n'
		.format(
			self.header_data('FONT_NAME'),
			self.header_data('DESIGNER'),
			self.header_data('FONT_PATH'),
			self.header_data('FONT_PATH'),
			self.header_data('UPM'),
			self.header_data('GLYPHS_VERSION'),
			self.header_data('CREATION_DATE'))
		)

	def report_header(self):
		self.report(self.header_doc(), init=True)

# ---- x ----
Glyphs.clearLog()
Glyphs.showMacroWindow()
f = Glyphs.font
myqa = QAEngine(f)
print(myqa.header_doc())
