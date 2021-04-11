#MenuTitle: Export Open Instances to InDesign 1.0
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__="""
Export all open instances in OTF in Indesign font's folder.
"""


import os, glob, shutil
from os.path import expanduser

# path to the folder where all files will be saved
home = expanduser("~")
desktop = '/Desktop/'
# folder = font.familyName
folder = 'exported_from_glyphs'
path = home+desktop+folder
indesign_folder = r'/Applications/Adobe InDesign CC 2015/Fonts/'

print(folder)

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

# change the all_files variable to indesign path
all_files = glob.glob(indesign_folder+folder+'/*')

# remove folder in InDesign path, if exists. Else, just move the folder from the desktop to InDesign font's folder
if os.path.exists(indesign_folder+folder):
	for files in all_files:
		os.remove(files)
	os.rmdir(indesign_folder+folder)
	shutil.move(path, indesign_folder)
else:
	shutil.move(path, indesign_folder)
	