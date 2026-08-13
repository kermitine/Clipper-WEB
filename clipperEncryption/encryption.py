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

def Encryption(word, seed, word_count):
    seeded_list = []
    encrypted_list = []
    pop_list = []
    word_list = [char.upper() for char in word] # converts word_list to uppercase

    for x in word_list:
        if x in nums:
            return ''.join(word_list)


    # CLIPPER VARIABLE CIPHERKEY CVC V2.0 (experimental)

    if word_count > 1:
        for x in range(word_count):
            seed = seed[-1:] + seed[:-1] 

    #---------------------------------------------

    for x in range(len(word_list)):
        if word_list[x] in special_characters_list:
            pop_list.append(x)

    pop_list.sort(reverse=True)
    for x in pop_list:
        word_list.pop(x)


    for char in word_list:
        if char == 'Z':
            seeded_list.append((seed[0]))
        else:
            window = character_window_index[char] # converts each 'letter' to its alphabetical index (A = 1, B = 2, etc)
            seeded_list.append(seed[window]) 
    for char in seeded_list:
            encrypted_list.append(character_window_inverse_index[char]) # converts the 1-26 seed back into a letter
    return ''.join(encrypted_list)
