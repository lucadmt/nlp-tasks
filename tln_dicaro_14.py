#!/usr/bin/env python3 

import math
import itertools
import functools
import pandas as pd
import common.utils as utils
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

punctuation = ['\'',']', '[', ',', '.', '(', ')', ';', '-', '*', '']
stop_words = set(stopwords.words('english'))
stop_words.add("'s")

data = pd.read_csv('./resources/wsketch_ententen_use.csv', sep=',')

len(data)

subj_lexnames = []
obj_lexnames = []

for i in data.subject:
    try:
        subj_lexnames.append(wn.synsets(i, wn.NOUN)[0].lexname())
    # WordNet doesn't have the correct senses for some words.
    except NameError as e:
        pass
    except IndexError as e1:
        pass

for i in data.object:
    try:
        obj_lexnames.append(wn.synsets(i, wn.NOUN)[0].lexname())
    # WordNet doesn't have the correct senses for some words.
    except NameError as e:
        pass
    except IndexError as e1:
        pass

print(f"unique supersenses for subjects: {len(set(subj_lexnames))}")
print(f"unique supersenses for objects: {len(set(obj_lexnames))}")
print('\n')
print(f"frequency of supersenses for subjects: {utils.word_frequencies(subj_lexnames)}")
print()
print(f"frequency of supersenses for objects: {utils.word_frequencies(obj_lexnames)}")