import os
import sys
import re

#F = Fungustober's notes for understanding how all this works while she edits this to support JSON files for the main file
#EDIT = Fungustober's marker for a part of code that needs edited to support JSON file

def convertList(setCode):
	#F: inputList = sets/SET-files/SET-raw.txt
    inputList = os.path.join('sets', setCode + '-files', setCode + '-raw.txt') #EDIT - needs changed from .txt to .json
	#F: outputList = lists/SET-list.txt
    outputList = os.path.join('lists', setCode + '-list.txt')
	#F: open up the inputList file
    with open(inputList, errors="ignore") as f:
		#F: now do the things
        raw = f.read()
		cards_raw = raw.replace('\n','NEWLINE').replace('REPLACEME','\\n') #EDIT - won't need this with the JSON file
	cards_raw = cards_raw.rstrip('\\n') #EDIT - also won't need this with the JSON file
	cards = cards_raw.split('\\n') #EDIT - will be able to replace this with a JSON crawler

    #F: array of cards to skip
	skipdex = []
    #F: This basically gets any alt-arts in a single set and adds their index to a list of cards to skip.
    #EDIT - we could probably do this a little better by going through the range of j,
    #and checking if the name of cards[j] == the name of cards[i] + token not in cards[j].shape and Basic not in cards[j].type
    #and instead of putting j in skipdex, we can put the card number of j in the skipdex, so we'd be able to iterate over the JSON cards array
	for i in range(len(cards)):
		tmpI = re.sub("\t[0-9]+\t.*", "", cards[i])
		for j in range(i):
			tmpJ = re.sub("\t[0-9]+\t.*", "", cards[j])
			if tmpI == tmpJ and "\ttoken\t" not in tmpJ and "\tBasic" not in tmpJ:
				skipdex.append(j)
	
	master_list = []
	cards_mono = []
	cards_multi = []
	cards_brown = []
	cards_land = []
	cards_basic = []
	cards_token = []
    
    #F: now go over the cards again
    #EDIT - iterate over the JSON cards array
	for i in range(len(cards)):
		#F: skip the card if it's in the skipdex
        if i in skipdex:
			continue
		card = cards[i].split('\t') #EDIT - won't need this with a JSON crawler
		# name to include card number
        #EDIT - replace the array indices with JSON keys; 0 = name; 4 = card number, 10 = shape
        #EDIT - we're going to remake this a little, instead of storing the name in the main list, we'll be storing a new json object with
            #name, number, and shape. I'll be figuring out how to do that once I get to working on updating this
		card[0] = card[4] + ('t_' if 'token' in card[10] else '_') + card[0]
		# card number to int
		card[4] = int(card[4]) #EDIT - we won't need to make it an int, because it will already be one in the JSON file afaik
		# filter sorting tags
		notes = card[len(card) - 1] #EDIT - replace the final index check with the JSON key
		if '!sort' in notes:
            #F: notes = index of !sort + 6 to the end of the string
			card[len(card) - 1] = notes[notes.index('!sort') + 6:]
		else:
			card[len(card) - 1] = 'zzz'

		# clean color inputs
        #EDIT - replace the array index with JSON keys; 1 = color
		if card[1] == 'WR':
			card[1] = 'RW'
		if card[1] == 'WG':
			card[1] = 'GW'
		if card[1] == 'UG':
			card[1] = 'GU'

		# clean color identity inputs
        #EDIT - replace the array index with JSON keys; 5 = color_identity
		if card[5] == 'WR':
			card[5] = 'RW'
		if card[5] == 'WG':
			card[5] = 'GW'
		if card[5] == 'UG':
			card[5] = 'GU'

		# clean rarities
        #EDIT - replace the array index with JSON keys; 2 = rarity
		if card[2] == 'common':
			card[2] = 4
		elif card[2] == 'uncommon':
			card[2] = 3
		elif card[2] == 'rare':
			card[2] = 2
		elif card[2] == 'mythic':
			card[2] = 1
		else:
			card[2] = 5

		# sort types
        #EDIT - replace the array index with JSON keys; 10 = shape, 1 = color, 3 = type
		if 'token' in card[10]:
			cards_token.append(card)
		elif len(card[1]) > 1:
			cards_multi.append(card)
		elif card[1] == '':
			if 'Basic' in card[3]:
				cards_basic.append(card)
			elif 'Land' in card[3]:
				cards_land.append(card)
			else:
				cards_brown.append(card)
		else:
			cards_mono.append(card)

	# prepare monocolor lists
	cards_w = []
	cards_u = []
	cards_b = []
	cards_r = []
	cards_g = []
	
    #EDIT - replace the array index with JSON keys
	for card in cards_mono:
		if card[1] == 'W':
			cards_w.append(card)
		if card[1] == 'U':
			cards_u.append(card)
		if card[1] == 'B':
			cards_b.append(card)
		if card[1] == 'R':
			cards_r.append(card)
		if card[1] == 'G':
			cards_g.append(card)

    row_count = max(len(cards_w),len(cards_u),len(cards_b),len(cards_r),len(cards_g))
    #F: put all the monocolor things into a big array
    cards_mono_arr = [cards_w, cards_u, cards_b, cards_r, cards_g]
	
	for x in range(len(cards_mono_arr)):
		card_arr = cards_mono_arr[x]
        #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
        #EDIT - replace them with the appropriate JSON keys
		cards_mono_arr[x] = sorted(card_arr, key=lambda x : (x[2], x[len(x) - 1], x[4]))
	
    #F: 'e' and 'er' are references to blank pngs for spoilers
	for row in range(row_count):
		for card_arr in cards_mono_arr:
			if (row >= len(card_arr)):
				master_list.append('e')
			else:
				#F: card_arr[row][0] = name
                #EDIT - replace it with the appropriate JSON key
                master_list.append(card_arr[row][0])

	for x in range(5):
		master_list.append('er')

	# prepare gold lists
	cards_wu = []
	cards_ub = []
	cards_br = []
	cards_rg = []
	cards_gw = []
	cards_wb = []
	cards_bg = []
	cards_gu = []
	cards_ur = []
	cards_rw = []
	cards_gold = []

    #EDIT - replace the index with a JSON key
	for card in cards_multi:
		if card[1] == 'WU':
			cards_wu.append(card)
		elif card[1] == 'UB':
			cards_ub.append(card)
		elif card[1] == 'BR':
			cards_br.append(card)
		elif card[1] == 'RG':
			cards_rg.append(card)
		elif card[1] == 'GW':
			cards_gw.append(card)
		elif card[1] == 'WB':
			cards_wb.append(card)
		elif card[1] == 'BG':
			cards_bg.append(card)
		elif card[1] == 'GU':
			cards_gu.append(card)
		elif card[1] == 'UR':
			cards_ur.append(card)
		elif card[1] == 'RW':
			cards_rw.append(card)
		else:
			cards_gold.append(card)
    
	# ally pairs
	row_count = max(len(cards_wu),len(cards_ub),len(cards_br),len(cards_rg),len(cards_gw))
	cards_ally_arr = [cards_wu, cards_ub, cards_br, cards_rg, cards_gw]

	for x in range(len(cards_ally_arr)):
		card_arr = cards_ally_arr[x]
        #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
        #EDIT - replace them with the appropriate JSON keys
		cards_ally_arr[x] = sorted(card_arr, key=lambda x : (x[2], x[len(x) - 1], x[4]))
	
    #F: 'e' and 'er' are references to blank pngs for spoilers
	for row in range(row_count):
		for card_arr in cards_ally_arr:
			if (row >= len(card_arr)):
				master_list.append('e')
			else:
				#F: card_arr[row][0] = name
                #EDIT - replace it with the appropriate JSON key
				master_list.append(card_arr[row][0])

	for x in range(5):
		master_list.append('er')

	# enemy pairs
	row_count = max(len(cards_wb),len(cards_bg),len(cards_gu),len(cards_ur),len(cards_rw))
	cards_enemy_arr = [cards_wb, cards_bg, cards_gu, cards_ur, cards_rw]

	for x in range(len(cards_enemy_arr)):
		card_arr = cards_enemy_arr[x]
        #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
        #EDIT - replace them with the appropriate JSON keys
		cards_enemy_arr[x] = sorted(card_arr, key=lambda x : (x[2], x[len(x) - 1], x[4]))
	
	for row in range(row_count):
		for card_arr in cards_enemy_arr:
			if (row >= len(card_arr)):
				master_list.append('e')
			else:
				#F: card_arr[row][0] = name
                #EDIT - replace it with the appropriate JSON key
				master_list.append(card_arr[row][0])

	for x in range(5):
		master_list.append('er')

	# 3c+ cards
    #F: x[1] = color, x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
    #EDIT - replace them with the appropriate JSON keys
	cards_gold = sorted(cards_gold, key=lambda x : (len(x[1]), x[2], x[len(x) - 1], x[4]))
    
	for card in cards_gold:
        #F: card_arr[row][0] = name
        #EDIT - replace it with the appropriate JSON key
		master_list.append(card[0])

	if len(cards_gold) % 5 != 0:
		for x in range(5 - (len(cards_gold) % 5)):
			master_list.append('e')

	if len(cards_gold) > 0:
		for x in range(5):
			master_list.append('er')

	# artifacts
	cards_brown = sorted(cards_brown, key=lambda x : (x[2], x[len(x) - 1], x[4]))

	for card in cards_brown:
		#F: card_arr[row][0] = name
        #EDIT - replace it with the appropriate JSON key
        master_list.append(card[0])

	if len(cards_brown) % 5 != 0:
		for x in range(5 - (len(cards_brown) % 5)):
			master_list.append('e')

	for x in range(5):
		master_list.append('er')

	# lands
	# prepare colored land lists
	lands_w = []
	lands_u = []
	lands_b = []
	lands_r = []
	lands_g = []
	lands_wu = []
	lands_ub = []
	lands_br = []
	lands_rg = []
	lands_gw = []
	lands_wb = []
	lands_bg = []
	lands_gu = []
	lands_ur = []
	lands_rw = []
	lands_other = []

    #F: 5 = Color Identity
    #EDIT - replace them with the proper JSON key
	for card in cards_land:
		if card[5] == 'W':
			lands_w.append(card)
		elif card[5] == 'U':
			lands_u.append(card)
		elif card[5] == 'B':
			lands_b.append(card)
		elif card[5] == 'R':
			lands_r.append(card)
		elif card[5] == 'G':
			lands_g.append(card)
		elif card[5] == 'WU':
			lands_wu.append(card)
		elif card[5] == 'UB':
			lands_ub.append(card)
		elif card[5] == 'BR':
			lands_br.append(card)
		elif card[5] == 'RG':
			lands_rg.append(card)
		elif card[5] == 'GW':
			lands_gw.append(card)
		elif card[5] == 'WB':
			lands_wb.append(card)
		elif card[5] == 'BG':
			lands_bg.append(card)
		elif card[5] == 'GU':
			lands_gu.append(card)
		elif card[5] == 'UR':
			lands_ur.append(card)
		elif card[5] == 'RW':
			lands_rw.append(card)
		else:
			lands_other.append(card)
	
	# monocolor
	row_count = max(len(lands_w),len(lands_u),len(lands_b),len(lands_r),len(lands_g))
	lands_mono_arr = [lands_w, lands_u, lands_b, lands_r, lands_g]

	for x in range(len(lands_mono_arr)):
        #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
        #EDIT - replace them with the appropriate JSON keys
		card_arr = lands_mono_arr[x]
		lands_mono_arr[x] = sorted(card_arr, key=lambda x : (x[2], x[len(x) - 1], x[4]))
	
	for row in range(row_count):
		for card_arr in lands_mono_arr:
			if (row >= len(card_arr)):
				master_list.append('e')
			else:
				#F: card_arr[row][0] = name
                #EDIT - replace it with the appropriate JSON key
				master_list.append(card_arr[row][0])

	# ally pairs
	row_count = max(len(lands_wu),len(lands_ub),len(lands_br),len(lands_rg),len(lands_gw))
	lands_ally_arr = [lands_wu, lands_ub, lands_br, lands_rg, lands_gw]

	for x in range(len(lands_ally_arr)):
        #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
        #EDIT - replace them with the appropriate JSON keys
		card_arr = lands_ally_arr[x]
		lands_ally_arr[x] = sorted(card_arr, key=lambda x : (x[2], x[len(x) - 1], x[4]))
	
	for row in range(row_count):
		for card_arr in lands_ally_arr:
			if (row >= len(card_arr)):
				master_list.append('e')
			else:
				#F: card_arr[row][0] = name
                #EDIT - replace it with the appropriate JSON key
				master_list.append(card_arr[row][0])

	# enemy pairs
	row_count = max(len(lands_wb),len(lands_bg),len(lands_gu),len(lands_ur),len(lands_rw))
	lands_enemy_arr = [lands_wb, lands_bg, lands_gu, lands_ur, lands_rw]

	for x in range(len(lands_enemy_arr)):
        #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
        #EDIT - replace them with the appropriate JSON keys
		card_arr = lands_enemy_arr[x]
		lands_enemy_arr[x] = sorted(card_arr, key=lambda x : (x[2], x[len(x) - 1], x[4]))
	
	for row in range(row_count):
		for card_arr in lands_enemy_arr:
			if (row >= len(card_arr)):
				master_list.append('e')
			else:
				#F: card_arr[row][0] = name
                #EDIT - replace it with the appropriate JSON key
				master_list.append(card_arr[row][0])

	if len(cards_land) - len(lands_other) > 0:
		for x in range(5):
			master_list.append('er')

	# other lands
    #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
    #EDIT - replace them with the appropriate JSON keys
	lands_other = sorted(lands_other, key=lambda x : (x[2], x[len(x) - 1], x[4]))

	for card in lands_other:
        #F: 0 = name
        #EDIT - replace it with the appropriate JSON key
		master_list.append(card[0])

	if len(lands_other) % 5 != 0:
		for x in range(5 - (len(lands_other) % 5)):
			master_list.append('e')

	if len(lands_other) > 0 and (len(cards_basic) > 0 or len(cards_token) > 0):
		for x in range(5):
			master_list.append('er')

	# basic lands
    #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
    #EDIT - replace them with the appropriate JSON keys
	cards_basic = sorted(cards_basic, key=lambda x : (x[2], x[len(x) - 1], x[4]))

	# if you're reading this, leave me alone, I did this in like 2 minutes I know it's bad code
    #F: well, I probably wouldn't be able to do much better to be completely fair
	basic_types = []
	for card in cards_basic:
        #F: 3 = type
        #EDIT - you know the deal
		if card[3] not in basic_types:
			basic_types.append(card[3])

	if len(basic_types) == 0:
		land_count = 0
	else:
		land_count = int(len(cards_basic) / len(basic_types)) # number of different basic arts
	for n in range(land_count): 
		for x in range(len(cards_basic)):
			if (x % land_count == n):
                #F: 0 = name
                #EDIT - you know the deal
				master_list.append(cards_basic[x][0])

	if len(cards_basic) % 5 != 0:
		for x in range(5 - (len(cards_basic) % 5)):
			master_list.append('e')

	if len(cards_basic) > 0:
		for x in range(5):
			master_list.append('er')

	# tokens
    #F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
    #EDIT - replace them with the appropriate JSON keys
	cards_token = sorted(cards_token, key=lambda x : (x[2], x[len(x) - 1], x[4]))

	for card in cards_token:
        #F: 0 = name
        #EDIT - you know the deal
		master_list.append(card[0])

	if len(cards_token) % 5 != 0:
		for x in range(5 - (len(cards_token) % 5)):
			master_list.append('e')

    #F: lists/SET-list.txt finally comes into play
    #F: \ufeff is the Byte Order Mark character that, according to Egg, was sneaking into card names and had to be forcibly removed
	with open(outputList, 'w') as f:
		for card_name in master_list:
			print(card_name.replace(u'\ufeff', ''), file=f)







#F: why are there so many blank lines down here





