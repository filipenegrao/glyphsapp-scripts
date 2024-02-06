#MenuTitle: Open all masters of a glyph to compare
# -*- coding: utf-8 -*-
__doc__="""

An easy way to open all masters of a selected glyph in the Text View.

"""


import random

f = Font
layer = f.selectedLayers[0]
glyph = layer.parent
masters_name = [master.name for master in f.masters]

# maybe useful 
glyph_name = glyph.name
glyph_category = glyph.category

folder_path = "./"
# those files above are mandatory. I'm using a MIT word list for the English words and a USP word list for Portuguese.
# https://www.mit.edu/~ecprice/wordlist.10000
en = "mit_most_used_en.txt"
# https://www.ime.usp.br/~pf/dicios/
pt = "usp_most_used_pt.txt"


def get_layer_masters(glyph):
	return [layer for layer in glyph.layers if layer.isMasterLayer]


def get_selected_glyph_layers():
	layer = Font.selectedLayers[0]
	return [l for l in glyph.layers if l.name in masters_name]


def get_word_layers(words):
	word_layers = []
	for word in words:
		for master in masters_name:
			for char in word:
				glyph_layers = get_layer_masters(f.glyphs[char])
				for layer in glyph_layers:
					if layer.name == master:
						word_layers.append(layer)
#		word_layers.append("\n")
	return word_layers


def load_words(filepath):
	with open(filepath, 'r') as f:
		return f.read().splitlines()


def filter_words_by_letter(words, letter):
	is_uppercase = letter.isupper()
	letter = letter.lower()
	if is_uppercase:
		return [word.capitalize() for word in words if word.lower().startswith(letter)]
	else:
		return [word for word in words if word.lower().startswith(letter)]


def random_pick(words, quantity=3):
	return random.sample(words, min(quantity, len(words)))

# change to 'pt' to open portuguese words
words = load_words(folder_path + en)
filtered_words = filter_words_by_letter(words, glyph_name)
# you can change et second parameter to define how many words will be open
selected_words = random_pick(filtered_words, 3)
print(selected_words)
print(get_selected_glyph_layers())


def open_tab(selected_list, word_list):
	joined_list = selected_list + word_list
	tab = f.newTab(joined_list)

open_tab(get_selected_glyph_layers(), get_word_layers(selected_words))