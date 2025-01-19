import os
import sys
import shutil
import json

import image_flip
import card_edge_trimmer
import list_to_list
import print_html_for_index
import print_html_for_search
import print_html_for_spoiler
import print_html_for_card
import print_html_for_set
import print_html_for_sets_page

#F = Fungustober's notes

def genAllCards(codes):
	file_input = {'cards':[]}
	#F: ...goes over all the set codes,
	for code in codes:
		#F: grabs the corresponding file,
		with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
			#F: puts its card data into a temp dictionary,
			raw = json.load(f)
			for card in raw['cards']:
				card['type'] = card['type'].replace('—', '-')
				fileinput['cards'].append(card)
	#F: opens a path,
	with open(os.path.join('lists', 'all-cards.json'), 'w', encoding='utf-8-sig') as f:
		#F: turns the dictionary into a json object, and puts it into the all-cards.json file
		#F: json.dump actually preserves the /n's and the //'s and whatnot, so we won't have to 
		json.dump(file_input, f)

#F: first, get all the set codes

set_codes = []
for entry in os.scandir('sets'):
	if entry.is_dir() and entry.name[-6:] == '-files':
		set_codes.append(entry.name[:-6])
	elif entry.name != 'README.md' and os.path.isfile(entry):
		os.remove(entry)

#F: sort them

set_codes.sort()

#F: then call a previously defined function, which...

genAllCards(set_codes)

#F: once that's done, it checks if a directory exists, ???, then makes that directory

if os.path.isdir('cards'):
	shutil.rmtree('cards')
os.mkdir('cards')

#F: iterate over set codes again
for code in set_codes:
	#F: it makes a directory at cards/SET
	os.mkdir(os.path.join('cards', code))

	#F: does something to all the images
	image_flip.flipImages(code)
	#F: makes a var = SET-files
	set_dir = code + '-files'
	#F: then look at /sets/SET-files/SET-trimmed.txt which is usually "false" and nothing else
	with open(os.path.join('sets', set_dir, code + '-trimmed.txt'), encoding='utf-8-sig') as f:
		trimmed = f.read()
		if trimmed == "false":
			#F: it makes sure it's false, then does something to the images
			card_edge_trimmer.batch_process_images(code)
			with open(os.path.join('sets', set_dir, code + '-trimmed.txt'), 'w') as file:
				file.write("true")
	#F: then sets it to "true", overwriting the old file

	#F: list_to_list.convertList is a long and important function
	list_to_list.convertList(code)
	
	custom_dir = os.path.join('custom', set_dir)
	if os.path.isdir(custom_dir):
		for file in os.listdir(custom_dir):
			filepath = os.path.join(custom_dir, file)
			destination = os.path.join('sets', set_dir)
			if os.path.isdir(filepath):
				destination = os.path.join(destination, file)
				if os.path.isdir(destination):
					shutil.rmtree(destination)
				shutil.copytree(filepath, destination)
			else:
				shutil.copy(filepath, destination)
			print(filepath + ' added')

	#F: more important functions
	if not os.path.exists(os.path.join('sets', code + '-files', 'ignore.txt')):
		print_html_for_spoiler.generateHTML(code, set_codes)
	print_html_for_set.generateHTML(code)

#F: grab lists/all-cards.txt & read it
with open(os.path.join('lists', 'all-cards.json'), encoding='utf-8-sig') as f:
	data = json.load(f)
#F: then the cards get put into an array
card_array = data['cards']
#F: iterate over the array
for card in card_array:
	card_name = card['card_name']
	with open(os.path.join('resources', 'replacechars.txt'), encoding='utf-8-sig') as f:
		chars = f.read()
	for char in chars:
		card_name = card_name.replace(char, '')
	#F: then open a path to cards/SET/NUM_NAME.json & write there
	with open(os.path.join('cards', card['set'], str(card['number']) + '_' + card_name + '.json'), 'w', encoding='utf-8-sig') as f:
		json.dump(card, f)
	#F: and then generate the html file for the card
	print_html_for_card.generateHTML(card)
print(f"HTML card files saved as cards/<set>/<card>.html")

custom_img_dir = os.path.join('custom', 'img')
if os.path.isdir(custom_img_dir):
	for file in os.listdir(custom_img_dir):
		filepath = os.path.join(custom_img_dir, file)
		destination = 'img'
		shutil.copy(filepath, destination)
		print(filepath + ' added')

print_html_for_sets_page.generateHTML(set_codes)
print_html_for_search.generateHTML(set_codes)
print_html_for_index.generateHTML(set_codes)







