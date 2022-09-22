#!/usr/bin/env python3

import time
import itertools
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
punctuation = ['\'',']', '[', ',', '.', '(', ')', ';', '-', '*', '', '\'\'', '``', ':', '?', '!', '$','’', '–', '‘', '“', '”']
stop_words = set(stopwords.words('english'))
stop_words.add("'s")

def append_results(anyobj, outfilename):
    out = open(outfilename, 'a')
    out.write(str(anyobj)+"\n\n\n")
    out.close()

def save_results(anyobj, outfilename):
    out = open(outfilename, 'w')
    out.write(str(anyobj))
    out.close()

def flatten(sl):
    return [j for i in sl for j in i]

def preprocess_phrase(phrase):
    """Preprocess a phrase, removing stopwords and punctuation, then does stemming on the obtained words
    Arguments:
        phrase: the phrase to preprocess
    Returns:
        A list of tokens"""
    return list(itertools.filterfalse(lambda i: i in stop_words or i in punctuation, [ps.stem(i.lower()) for i in word_tokenize(phrase)]))

def preprocess_phrase_nostem(phrase):
    """Preprocess a phrase, removing stopwords and punctuation
    Arguments:
        phrase: the phrase to preprocess
    Returns:
        A list of tokens"""
    return list(itertools.filterfalse(lambda i: i in stop_words or i in punctuation, [i.lower() for i in word_tokenize(phrase)]))

def word_frequencies(wordlist):
    """Given a list of words, calculate the frequency of each one, and map the set of words in wordlist to their frequency
    Arguments:
        wordlist: A list of words in the concept(s) definition
    Returns:
        A list of tuples: (token, frequency)"""
    wordset = list(set(wordlist))
    return list(reversed(sorted(list(map(lambda i: (i, wordlist.count(i)), wordset)), key = lambda x: x[1])))

def gen_combo(set1, set2):
    """Generate combinations from 2 sets, a word from the first, the second from the second.
    Arguments:
        set1: The first set of words (tokens)
        set2: The second set of words (tokens)
    Returns:
        A set of tuples in which the first component belongs to set1, the second to set2"""
    result_set = []
    for i in set1:
        for j in set2:
            result_set.append((i, j))
    return set(result_set)

def profile(function):
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time  = time.time()
        duration = (end_time - start_time)
        f_name = function.__name__
        print(f"{f_name} took {duration:.3f}s")

        return result
    return wrap
