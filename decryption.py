

import os
import re
import copy
import pprint
from operator import itemgetter
from collections import OrderedDict


alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
symbols = [' ', '.', ',', ';', '-', '\n', '\r', "'"]
freq = ['E', 'A', 'T', 'O', 'N', 'H', 'I', 'R',
        'S', 'D', 'L', 'F', 'W', 'M', 'U', 'G',
        'C', 'Y', 'P', 'B', 'K',
        'V', 'J', 'X', 'Q', 'Z']
generated_patterns = {}


def get_freq(cipher):
    storage = {}
    rawfile = get_text_data(cipher)
    rawfile = rawfile.lower()

    for char in rawfile:
        if char in symbols:
            continue
        if char not in storage:
            storage[char] = 1
        else:
            storage[char] += 1

    return storage


def dictionary_sort(freq_ed):
    storage = get_freq(freq_ed)

    s= (OrderedDict(sorted(storage.items(), key = itemgetter(1), reverse = True)))

    new_list = list()
    for i in s.keys():
        new_list.append(i)

    return new_list


def get_pattern(text):
    text = text.upper()
    next_num = 0
    char_num = {}
    pattern = []

    for char in text:
        if char not in char_num:
            char_num[char] = str(next_num)
            next_num += 1
        pattern.append(char_num[char])
    return '.'.join(pattern)


def generate_word_pattern_list():
    gen_patterns = {}
    file = open('caps.txt')
    en_dict = file.read().split('\n')
    file.close()

    for word in en_dict:
        pattern = get_pattern(word)

        if pattern not in gen_patterns:
            gen_patterns[pattern] = [word]
        else:
            gen_patterns[pattern].append(word)
    return gen_patterns


def get_text_data(filename: str) -> str:
    with open(filename, 'rb') as data:
        res = data.read()
    return bytes.decode(res.upper())


def empty_map():
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [],
            'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [],
            'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': []}


def add_to_map(char_map, cipher, x):
    char_map = copy.deepcopy(char_map)
    for i in range(len(cipher)):
        if x[i] not in char_map[cipher[i]]:
            char_map[cipher[i]].append(x[i])
    return char_map


def inter_map(map_1, map_2):
    x_map = empty_map()
    for char in alphabet:

        if map_1[char] == []:
            x_map[char] = copy.deepcopy(map_2[char])
        elif map_2[char] == []:
            x_map[char] = copy.deepcopy(map_1[char])
        else:
            for mapped_char in map_1[char]:
                if mapped_char in map_2[char]:
                    x_map[char].append(mapped_char)

    return x_map


def remove_from_map(char_mapping):
    char_mapping = copy.deepcopy(char_mapping)
    loop = True
    while loop:
        loop = False
        solved = []
        for cipher_char in alphabet:
            if len(char_mapping[cipher_char]) == 1:
                solved.append(char_mapping[cipher_char][0])
        for cipher_char in alphabet:
            for s in solved:
                if len(char_mapping[cipher_char]) != 1 and s in char_mapping[cipher_char]:
                    char_mapping[cipher_char].remove(s)
                    if len(char_mapping[cipher_char]) == 1:
                        loop = True
    return char_mapping


def substitution(msg):
    x_list = generate_word_pattern_list()
    y_map = empty_map()
    cleanup = re.compile('[^A-Z\s]')
    cipher_list = cleanup.sub('', msg.upper()).split()
    for cipher in cipher_list:
        new_map = empty_map()

        char = get_pattern(cipher)
        if char not in x_list:
            continue

        for x in x_list[char]:
            new_map = add_to_map(new_map, cipher, x)

        y_map = inter_map(y_map, new_map)

    return remove_from_map(y_map)


def decrypt_freq(cipher, new_freq):
    for i in range(len(new_freq)):
        print(new_freq[i] + " ==> " + freq[i])
        cipher = cipher.replace(new_freq[i], freq[i])
    print(cipher)


def decrypt(key, message):
    msg = ''
    x = key
    y = alphabet

    for symbol in message:
        if symbol.upper() in x:
            char = x.find(symbol.upper())
            if symbol.isupper():
                msg += y[char].upper()
            else:
                msg += y[char].lower()
        else:
            msg += symbol

    return msg


def cruncher(cipher, map_char):
    key = ['*'] * len(alphabet)
    for cipher_char in alphabet:
        if len(map_char[cipher_char]) == 1:
            key_index = alphabet.find(map_char[cipher_char][0])
            key[key_index] = cipher_char
            # print(key)
        else:
            cipher = cipher.replace(cipher_char.lower(), '_')
            cipher = cipher.replace(cipher_char.upper(), '_')
    key = ''.join(key)
    print('Key: ')
    print(key)
    return decrypt(key, cipher)


def main():
    print()
    file = input("Enter a file name of your ciphertext (should be located in same directory as this program): ")
    message = get_text_data(file)
    menu = input("Select method. \n 1.Analysis (FAST - Not Universal) \n "
                 "2.Dictionary (SLOW - Universal can work with any cipher)\n >>>")

    if menu == '2':
        print()
        print('This can take some time (1-2 mins)...')
        print()
        map_chart = substitution(message)
        print('Map:')
        pprint.pprint(map_chart)
        # print()
        # print('Original ciphertext:')
        # print(message)
        print()
        print('("*" means that character wasn''t found due to short cipher)')
        final_result = cruncher(message, map_chart)
        print()
        print(final_result)
    else:
        message = message.lower()
        new_freq = (dictionary_sort(file))
        decrypt_freq(message, new_freq)


main()
