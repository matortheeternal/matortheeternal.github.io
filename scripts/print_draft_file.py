import os
import sys
import json
import re

#F = Fungustober's notes
def filtered(card, filters):
	for f in filters:
		if ('!' + f) in card['notes']:
			return True
	return False

def generateFile(code):
	with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as j:
		set_data = json.load(j)

	structure_path = os.path.join('resources', set_data['draft_structure'].replace(' ','-') + '-structure.json')
	if os.path.isfile(os.path.join('sets', code + '-files', 'structure.json')):
		structure_path = os.path.join('sets', code + '-files', 'structure.json')
	with open(structure_path, encoding='utf-8-sig') as j:
		structure = json.load(j)

	filters = []
	booster = {}

	github_path = os.path.split(os.getcwd())[1] # this gets the current working directory, so it's an easy failcase

	for slot in structure:
		booster[slot['name']] = []
		if slot['filtered']:
			filters.append(slot['name'])

	draft_string = '''[CustomCards]
	[
	'''

	for x in range(len(set_data['cards'])):
		card = set_data['cards'][x]
		# clean hybrids
		h_pattern = r'\{([A-Z0-9])([A-Z])\}'
		h_replace = r'{\1/\2}'
		if re.search(r'token', card['type']):
			continue

		for slot in structure:
			slot_name = slot['name']
			if slot_name in [ 'wildcard', 'foil' ] and not filtered(card, filters) and not 'Basic' in card['type'] and not 'token' in card['shape']:
				booster[slot_name].append(card)
			elif not slot['custom']:
				if ((card['rarity'] == 'mythic' and slot_name == 'rare') or card['rarity'] == slot_name) and not filtered(card, filters) and not 'Basic' in card['type'] and not 'token' in card['shape']:
					booster[slot_name].append(card)
			else:
				if ('!' + slot_name) in card['notes']:
					booster[slot_name].append(card)

		draft_string += '''	{
			"name": "''' + card['card_name'] + '''",
			"rarity": "''' + ('special' if card['rarity'] == 'cube' else card['rarity']) + '''",
			"mana_cost": "''' + re.sub(h_pattern, h_replace, card['cost']) + '''",
			"type": "''' + card['type'] + '''",
			"collector_number": "''' + str(card['number']) + '''",
	'''

		card_file_name = (str(card['number']) + '_' + card['card_name']) if ('image_name' not in set_data or set_data['image_name'] != 'position') else card['position']
		if 'double' in card['shape']:
			draft_string += '''		"back": {
				"name": "",
				"type": "",
				"image_uris": {
					"en": "https://''' + github_path + '''/sets/''' + code + '''-files/img/''' + card_file_name + '''_back.''' + set_data['image_type'] + '''"
				}
			},
			"image_uris": {
				"en": "https://''' + github_path + '''/sets/''' + code + '''-files/img/''' + card_file_name + '''_front.''' + set_data['image_type'] + '''"
			}
		},
	'''
		else:
			draft_string += '''		"image_uris": {
				"en": "https://''' + github_path + '''/sets/''' + code + '''-files/img/''' + card_file_name + '''.''' + set_data['image_type'] + '''"
			}
		}''' + (''',''' if x != len(set_data['cards']) - 1 else '''''') + '''
	'''

	draft_string += ''']

'''
	
	p1p1 = []
	for slot in structure:
		slot_list = []
		draft_string += '''[''' + slot['name'] + '''(''' + str(slot['count']) + ''')]
'''
		for c in booster[slot['name']]:
			count = -1
			if slot['balanced'] == 'b': # normal distribution
				match c['rarity']:
					case 'mythic':
						count = 1
					case 'rare':
						count = 2
					case 'uncommon':
						count = 4
					case 'common':
						count = 8
			elif slot['balanced'] == 'w': # wildcard distribution
				# these numbers look weird but they distribute to 0.6 u / 0.2 c / 0.17 r / 0.03 m (I did the math)
				match c['rarity']:
					case 'mythic':
						count = 4
					case 'rare':
						count = 7
					case 'uncommon':
						count = 15
					case 'common':
						count = 6
			elif slot['balanced'] == 'f': # foil distribution
				# ditto, except 0.57 c / 0.35 u / 0.07 r / 0.01 m
				match c['rarity']:
					case 'mythic':
						count = 1
					case 'rare':
						count = 2
					case 'uncommon':
						count = 6
					case 'common':
						count = 12
			elif slot['balanced'] == 'c': # cube distribution
				count = 1
			else:
				count = 5

			if count > 0:
				draft_string += '''	''' + str(count) + ''' ''' + c['card_name'] + '''
'''
		for x in range(slot['count']):
			p1p1.append(slot_list)

	with open(os.path.join('sets', code + '-files', code + '-draft.txt'), 'w', encoding='utf-8-sig') as f:
		f.write(draft_string)

