#MenuTitle: Export Open Instances 1.0
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__="""
Export all open instances in OTF.
"""

import os, glob
from os.path import expanduser

# path to the folder where all files will be saved
home = expanduser("~")
desktop = '/Desktop/'
folder = 'exported_fonts'
path = home+desktop+folder

# check if the folder already exists. If not, create the folder
if os.path.exists(path):
	print('The %s already exists in %s' %(folder, path))
else:
	os.mkdir(path)
	print('Folder %s created in %s' %(folder, path))

# remove all files before save the new ones
all_files = glob.glob(path+'/*')
for files in all_files:
	os.remove(files)
	 
# check for all open fonts and export all instances to the created folder
for font in Glyphs.fonts:
	for instance in font.instances:
		instance.generate(FontPath = path)
	Glyphs.showNotification('Export fonts', 'The fonts were exported successfully.')

	