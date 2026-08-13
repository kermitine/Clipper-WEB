"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the Clipper project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vars.ifArray import *
from vars.seedGenVars import *
from vars.globalVars import *

def seedGeneration(seed_word):
    seed = []
    num_dict = 1
    pop_list = []
    special_chars = 0

    print('Starting seed generation...')

    time.sleep(gap_time)

    seed_word_list = [x.upper() for x in seed_word] # splits seed_word into uppercase list
    for x in range(len(seed_word_list)):
        if seed_word_list[x] in special_characters_list or seed_word_list[x] == ' ' or seed_word_list[x] in nums:
            if special_chars < 1:
                print('Purging numbers and special characters')
            pop_list.append(x)
            special_chars += 1

    time.sleep(gap_time)

    pop_list.sort(reverse=True)

    for x in pop_list:
        seed_word_list.pop(x)


    scramble_times = seed_generation_index_int[seed_word_list[len(seed_word_list)-1]]
    print('Scrambling')
    for x in range(scramble_times):
        seed_word_list = seed_word_list[-1:] + seed_word_list[:-1] 

    if len(seed_word_list) > 26:
        print('Word sliced')
        seed_word_list = seed_word_list[:26]

    time.sleep(gap_time)

    seed_word_list = list(dict.fromkeys(seed_word_list))  # removes duplicate letters (no idea how this works but it does)

    print('Purging duplicates')

    for char in seed_word_list: # uses seed_generation__index dict to convert letter to number
        seed.append(seed_generation_index[char])

    print('Converting text to numerics')

    time.sleep(gap_time)

    if len(seed) < 26: # if seed is not long enough
        while len(seed) < 26:
            if num_dict > 26:
                num_dict = 1
            if seed_generation_number_index[num_dict] not in seed:
                seed.append(seed_generation_number_index[num_dict])
                num_dict += 1
                pass
            num_dict += 1

    print('Verifying...')

    time.sleep(gap_time)
    print(''.join(seed))
    print('Seed generated successfully.' + '\n')
    return seed
