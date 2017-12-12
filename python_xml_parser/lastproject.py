# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import string
import nltk

tree1 = ET.parse('ProjectBiblicalTerms.xml')
root1 = tree1.getroot()

tree2 = ET.parse('BiblicalTermsHii.xml')
root2 = tree2.getroot()

main_dict = {'06500100100':{'Christ.2.2':['यीशु मसीह', 'यीशु']}} # to store the final output
term_dict = {} # to save the bible terms and their Hindi transliteration
term_reference_dict = {}
# The terms and the transliteration are generatedTermRendering first

for renders in root2[0]:    #root2[0] is the tag TermRendering object in BiblicalTermsHii
    Id = renders.find('Id').text    # Id tag conatins the term
    renderings = renders.find('Renderings').text  #Renderings contain the transliterated terms
    
    if renderings != None:
        translation_words = [renderings]
    else:
        translation_words = [renderings]
    term_dict[Id] = renderings


for t in root1.findall('Term'):
    word = t.find('Transliteration').text   #This is the term word
    term_reference_list = []
    for v in t[3]:
        verse_code = v.text # The code of the verse
        term_reference_list.append(verse_code)
        if verse_code not in main_dict: # If a verse code is not in the main_dict, then insert it directly without having to check
            main_dict[verse_code] = {word: term_dict[word]}
        else: # If the verse code is already in then it needs to be added to the value of the main_dict[verse_code]
            temp_dict = main_dict[verse_code]
            temp_dict[word] = term_dict[word]
            main_dict[verse_code] = temp_dict
    term_reference_dict[word] = term_reference_list

books = {"1": "GEN", "2": "EXO", "3": "LEV", "4": "NUM", "5": "DEU", "6": "JOS", "7": "JDG", "8": "RTH", "9": "1SA", "10": "2SA", "11": "1KI", "12": "2KI", "13": "1CH", "14": "2CH", "15": "EZR", "16": "NEH", "17": "EST", "18": "JOB", "19": "PSA", "20": "PRO", "21": "ECC", "22": "SNG", "23": "ISA", "24": "JER", "25": "LAM", "26": "EZE", "27": "DAN", "28": "HOS", "29": "JOE", "30": "AMO", "31": "OBA", "32": "JON", "33": "MIC", "34": "NAH", "35": "HAB", "36": "ZEP", "37": "HAG", "38": "ZEC", "39": "MAL", "40": "MAT", "41": "MAR", "42": "LUK", "43": "JHN", "44": "ACT", "45": "ROM", "46": "1CO", "47": "2CO", "48": "GAL", "49": "EPH", "50": "PHL", "51": "COL", "52": "1TH", "53": "2TH", "54": "1TI", "55": "2TI", "56": "TIT", "57": "PHM", "58": "HEB", "59": "JAS", "60": "1PE", "61": "2PE", "62": "1JO", "63": "2JO", "64": "3JO", "65": "JUD", "66": "REV"}
books_inverse = {v:k for k,v in books.items()} 

def check_pattern(tr_word, tr_wordlist):
    'Checks if a word selected from the usfm file has a match from the translated word list'
    # pdb.set_trace()
    if tr_wordlist:
        translations_list = []
        for wi in tr_wordlist:
            match = re.search(tr_word, wi)
            if match:
                pattern = match.group()
                translations_list.append(pattern)
        joined_words = ', '.join(translations_list)
        return joined_words
    else:
        return None

def digit_lenght_check(num):
    '''to convert all book, chapter and verse codes to 3 digit values
     to match the verse code from the "ProjectBiblicalTerms" file'''
    if len(num) == 1:
        return '00' + num
    else:
        return '0' + num

def tag_format(words, code, verse_list):
    'adds the tagging format to a word and returns the value'
    previous_index = None
    next_index = None
    if code in verse_list:
        index_value = verse_list.index(code)
        if index_value == 0:
            next_index = index_value + 1
        elif index_value > 0 and (index_value + 1) == len(verse_list):
            previous_index = index_value - 1
        else:
            previous_index = index_value - 1
            next_index = index_value + 1
    else:
        previous_index = None
        next_index = None

    if previous_index is not None:
        previous_code = books[str(int(verse_list[previous_index][0:3]))] + ' ' + str(int(verse_list[previous_index][3:6])) + ':' + str(int(verse_list[previous_index][6:9]))
    else:
        previous_code = ''
    if next_index is not None:
        next_code = books[str(int(verse_list[next_index][0:3]))] + ' ' + str(int(verse_list[next_index][3:6])) + ':' + str(int(verse_list[next_index][6:9]))
    else:
        next_code = ''
    formatted = "\\f + \\fr ch:" + str(words) +" \\ft Previous: " + str(previous_code) + "; Next: " + str(next_code) + "\\ft*"
    return formatted

def verse_handler(code, verse):
    'Returns a string back starting in the format "\\v (digit)"'
    verse_num = str(int(code[6:9]))
    final_verse = '\\v ' + str(verse_num) + ' ' + verse
    return final_verse

def add_tags(verse_code, verse):
    'returns a text with the tags added to it.'
    
    punct_handler = re.sub(r'\s([' + string.punctuation +'])', r'SPT\1', verse)
    punct_handler = re.sub(r'([' + string.punctuation +'])\s', r'\1SPT', punct_handler)
    punct_handler = re.sub(r'([' + string.punctuation +'])', r' \1 ', punct_handler)  #SPT is a marker
    word_list = nltk.word_tokenize(punct_handler)
    main_word_list = []
    for wi in word_list:
        for k, v in main_dict[verse_code].items():
            tranlsation_words = check_pattern(wi, v)    #Recieves all the available translations/interpretations of the word, if any.
            if tranlsation_words:
                verse_text = wi + tag_format(tranlsation_words, verse_code, term_reference_dict[k]) #wi is the actual word and tag_format() returns a text with information of the previous and next occurences.
                main_word_list.append(verse_text)
            else:
                main_word_list.append(wi)
    join_main_word_list = " ".join(main_word_list)
    main_word_text = re.sub(r'\s([' + string.punctuation + '])\s', r'\1', join_main_word_list)
    main_word_text = re.sub(r'SPT', '', main_word_text)
    return main_word_text

import pdb
def usfm_handler(filename):
    'To process the usfm files'
    # pdb.set_trace()
    open_file = open(filename, 'r')
    file_text = open_file.read()
    main_text_list = [] 
    chapter_pattern = re.compile('(\\c )(\d+)')
    book_name = re.search('(?<=\id )\w{3}', file_text).group(0)
    book_num = books_inverse[book_name]
    book_code = digit_lenght_check(book_num)
    split_usfm = file_text.split('\\c')
    i = 0
    for chapter_text in split_usfm:
        if i == 0:
            main_text_list.append(chapter_text)
            i += 1
            continue
        else:
            # pdb.set_trace()
            chapter_text = "\\c" + chapter_text
            chapter_number = re.search(chapter_pattern, (chapter_text.split('\n')[0])).group(2)
            chapter_code = digit_lenght_check(chapter_number)
            verse_pattern = re.compile(r'(\\v )(\d+)')
            # pdb.set_trace()
            split_text = chapter_text.split('\n')
            split_text.pop(-1)
            print (split_text)
            for line in split_text:

                
                result = re.match(verse_pattern, line)
                if result:
                    reference_code = digit_lenght_check(line[3:4])
                    verse = line[4:]
                    verse_sub = re.sub(verse_pattern, r'' + str(book_code) + str(chapter_code) + str(reference_code) + '00', line)
                    verse_code = verse_sub[0:11]
                    print (verse_code)
                    
                    filtered_line = add_tags(verse_code, verse)
                    # print (filtered_line)
                    actual_verse = verse_handler(verse_code, filtered_line)  # A verse line as how it appears on the usfm file
                    main_text_list.append(actual_verse)
                else:
                    main_text_list.append(line)
        # i += 1
    final_text = "\n".join(main_text_list)
    open_file = open('output' + str(filename), 'w')
    open_file.write(final_text)
    return 'finished'

usfm_handler('66_JUD-OA-HIN.usfm')