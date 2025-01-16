import os
import sys
import shutil

import image_flip
import card_edge_trimmer
import list_to_list
import print_html_for_index
import print_html_for_search
import print_html_for_spoiler
import print_html_for_card
import print_html_for_set
import print_html_for_sets_page

#F = Fungustober's notes for understanding how all this works while she edits this to support JSON files for the main file
#EDIT = Fungustober's marker for a part of code that needs edited to support JSON file

def genAllCards(codes):
	file_input = '' #EDIT - change this to `file_input = "{\"meta\":{},\"data\":{"`
    #F: ...goes over all the set codes
	for code in codes:
        #F: grabs the corresponding file
        with open(os.path.join('sets', code + '-files', code + '-raw.txt'), encoding='utf-8-sig') as f:#EDIT - need to change file ending to .json
			#F: puts it into a temp variable
            raw = f.read()
            #EDIT - add in a system that "husks" each of the .json files (i.e. removes the {\"meta\":{},\"data\":{ part from the front 
            #and the }} from the back) so they can be stitched together into one file. They'll also need commas between them.
            #F: then adds it to a more global variable
			file_input += raw.replace('\n','NEWLINE').replace('REPLACEME','\\n')#EDIT - won't be needed when the json file is used
    #F: and once that's done, it removes the final newline in the file
	file_input = file_input.removesuffix('\\n') #EDIT - change this to .removesuffix(',')

    #F: then opens a path
    #EDIT - change this to all-cards.json
	with open(os.path.join('lists', 'all-cards.txt'), 'w', encoding='utf-8-sig') as f:
    #F: and puts the text into the path
		f.write(file_input.replace('—', '–'))

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

    #F: this is where 90% of the actual processing seems to happen. We'll need to comment list_to_list.py as well. This...
	list_to_list.convertList(code)
    
    #F: then it tries to find /custom/SET-files/ and I don't think the rest of this is relevant to me
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

    #F: I think this is also not relevant to me
    #F: Actually, thinking about it, print_html_for_spoiler does sound like something that involves me
    #F: same with print_html_for_set
	if not os.path.exists(os.path.join('sets', code + '-files', 'ignore.txt')):
		print_html_for_spoiler.generateHTML(code, set_codes)
	print_html_for_set.generateHTML(code)

#F: but this is
#F: grab lists/all-cards.txt & read it
with open(os.path.join('lists', 'all-cards.txt'), encoding='utf-8-sig') as f:
	cards = f.read()
#F: idk the order this happens in, but a bunch of things get replaced
cards = cards.replace('\n','NEWLINE').replace('REPLACEME','\\n').rstrip('\\n') #EDIT - won't be needed with the json file
#F: then the cards get put into an array
card_array = cards.split('\\n') #EDIT - change this to a JSON crawler
#F: iterate over the array
for card in card_array:
    #F: split each card based on the tabs
	card_stats = card.split('\t') #EDIT - won't be needed with the JSON crawler
    #F: card_name is the first thing of the array
	card_name = card_stats[0] #EDIT - this will be slightly easier with JSON
	#F: then do some more stuff that I don't think I need to bother with
    with open(os.path.join('resources', 'replacechars.txt'), encoding='utf-8-sig') as f:
		chars = f.read()
	for char in chars:
		card_name = card_name.replace(char, '')
    #F: then open a portal to cards/SET/NUM_NAME.txt & write there
    #EDIT - make those point to the named JSON keys instead of the array indices
	with open(os.path.join('cards', card_stats[11], card_stats[4] + '_' + card_name + '.txt'), 'w', encoding='utf-8-sig') as f:
		f.write(card)
	#F: and then generate the html file for the card
    print_html_for_card.generateHTML(card) #F: looks like we'll need to study print_html_for_card.generateHTMl as well
print(f"HTML card files saved as cards/<set>/<card>.html")

#F: and then I think this doesn't involve me
custom_img_dir = os.path.join('custom', 'img')
if os.path.isdir(custom_img_dir):
	for file in os.listdir(custom_img_dir):
		filepath = os.path.join(custom_img_dir, file)
		destination = 'img'
		shutil.copy(filepath, destination)
		print(filepath + ' added')

#F: and I'll have to investigate these too.
print_html_for_sets_page.generateHTML(set_codes)
print_html_for_search.generateHTML(set_codes)
print_html_for_index.generateHTML(set_codes)







