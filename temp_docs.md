# About
This repository is a collection of useful (or not) Glyphs App's scripts. Check out how some of then works in https://vimeo.com/album/4932608

Drop me a line if you need any help.

## Data Extractors
**Save vertical metrics data**: Takes the vertical metrics data and saves in a .cvs file for further analysis. I wrote this to compare the data between typefaces of the same style.

## Diacritics & Combs
**Change the LSB and RSB for all comb glyphs**: Simply change the metric values for comb marks. It is set by default as 50 units (zero, maybe?), but can be modified for whatever you prefer. You just have to change the values layer.LSB and layer.RSB.
	
**Narrow Diacritics maker (in progress)**: Duplicates "dieresiscomb", "gravecomb", "acutecomb", "brevecomb", "tildecomb", "macroncomb", "ogonekcomb" addind a ".narrow" suffix.

**Open all comb marks in a new tab**: Open all combs in a new tab based on its category (*Mark*) and subcategory (*Nonspacing*). Simple as that.

**Open all comb marks in a new tab**: Open all the glyphs related to some glyph. E.g., select tilde and run and all the glyphs inside your font that has a tilde name on it will be open.

**Delete all anchors from current glyph**: Remove all anchors from current, selected glyph.

## Guides
**Label Guidelines**: (GUI) Label Guidelines was written to (apparently) add labels to Guidelines. Additionally, it has the option to delete all guides (local or global). Vanilla required.

![label-guidelines-glyphs-script](img/guideline.png)

## Italics
**Slant Glyphs:** (GUI) Based on Cyrus Highsmith and David Jonathan Ross's Italic Bowtie for Robofont, this tool is build to slant all selected glyphs in Edit View while adds a copy of the Roman version in the background. It's not supposed to be an automatic italic solution but gives you a head start. Vanilla required. **Warning:** this script erases all the layers in the background that was previously there. Comment the following line to avoid that: background_layer.paths = []


![slant-glyphs-script](img/slant.png)

## Kerning
**Create kerning groups for ligatures**: Search for all 'dligs' and set its kerning groups according to its reference glyphs.

**Important:** This script relies on Georg's script 'Diacritic Ligature Maker.py' so the must be together like Siamese twins.
	 
## Paths
**Change Ascenders & Descenders:** This code changes the height of ascenders or descenders of selected glyphs in Edit View. To the script work properly, your overshoot parameter should be configured for, at least, the same as your highest overshoot (maybe I should have called this parameter as tolerance. Feel free to change that for me!)

**Pro tip:** Use Arrows Up and Down as shortcuts.

![change-ascenders-descenders-glyphs-script](img/ascender_descender.png)

## Workflow
**Brand New Day**: This script creates a new folder named the current date (Y-M-D format) with all the same stuff you have inside the existing file's folder, including py scripts or anything you have on your glyphs file's folder. Then, the code closes the opened file and opens the new one. Based on Hannes Famira's workflow, which was type design instructors on Type@Cooper 2017.

**Brand New Day With Log**: The difference between this script and the previous one is that this creates and writes a log file (.md and .txt) on the root folder.

**Export All Open Fonts**: (GUI) This script export all open fonts (instances inside fonts, to be precise) to a selected folder. The default folder is configured to ~/Library/Application Support/Adobe/Fonts. Vanilla required.

![export-all-open-fonts-glyphs-script](img/export_all.png)

**Export All Open Fonts to UFO**: (GUI) For those folks into a UFO's workflow.

**Open Selected Glyphs In A New Tab**: I've always found myself very annoyed by clicking some glyphs in the Font Panel and only one of then open. I'm not sure if it is my inability or something else, but the idea behind this few lines is to open all the glyphs selected, regardless of your ability.
 
**Set color for current tab**: This script all about creates an *opt-cmd-r* shortcut for changing the color. Change R, G, B, A to your favorite color.

**Start a new project**: This is not a Glyphs App script per se. If you have the same folder structure for every project, this script creates that structure in a breeze. Just edit the FOLDERS list to change my current arrangement, that has the following subfolders: critiques, mockups, proofs, fonts, sources, research, data, sketches.

## Installation

Put the scripts inside the Scripts folder (Script > Open Scripts Folder or Cmd+Shift+Y). Then, hold down the Option key and choose Script > Reload Scripts (Cmd+Opt+Shift+Y). The scripts should appear in the Script menu.

Some of those tools required Vanilla to work. To install the Vanilla module, go to Glyphs > Preferences... > Add-ons > Modules > Install Modules.

## Troubleshooting
Please report any issues or pull requests here in GitHub. Don't forget to indicate your OS X and Glyphs App version.

## Requirements
These scripts were tested using 2.5 and Mac OS 10.13. They should work on any Glyphs 2.x, but might requires some changes.

## License
Copyright (c) 2015–18 Filipe Negrão (@filipenegrao). It has some code samples by Georg Seifert (@schriftgestalt) and Rainer Erich Scheichelbauer (@mekkablue) that were posted in [Glyphs' App Forum] (https://glyphsapp.com/forum).

Licensed under the Apache License, Version 2.0 (the "License"); you may not use the software provided here except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
