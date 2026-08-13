"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the Clipper project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vars.ifArray import *
from vars.seedGenVars import *


def Decryption(word, seed, word_count):
    seed_index_list = []
    letter_index_list = []
    decrypted_word_list = []
    
    word = word.upper()

    for x in word:
        if x in nums:
            return word

    
    # CLIPPER VARIABLE CIPHERKEY CVC V2.0 (experimental)

    if word_count > 1:
        for x in range(word_count):
            seed = seed[-1:] + seed[:-1] 

    #---------------------------------------------


    for char in word:
        letter_index_list.append(character_window_index_str[char])
    for letter_index in letter_index_list:
        for seed_index in range(len(seed)):
            if letter_index == seed[seed_index]: # if the alphabetical index of the letter matches the seed, take the index of the seed
                seed_index_list.append(seed_index)
                break
    for num in seed_index_list:
        if num == 'Z':
            decrypted_word_list.append('Z')
        else:
            decrypted_word_list.append(character_window_inverse_index_int[num])
    return ''.join(decrypted_word_list)


