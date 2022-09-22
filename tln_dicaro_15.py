#!/usr/bin/env python3 

import math
import itertools
import functools
import pandas as pd
import common.utils as utils
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

punctuation = ['\'',']', '[', ',', '.', '(', ')', ';', '-']
stop_words = set(stopwords.words('english'))
stop_words.add("'s")

definitions = "./resources/defs.csv"
data = pd.read_csv(definitions)

# Parameter that controls in how many phrases should a word appear, before not being considered a stopword
# Coherent results are with values >= 3
stopwords_treshold = 3

# Variante di preprocessing che non usa stemming
def preprocess_phrase(phrase):
    """Preprocess a phrase, removing stopwords and punctuation
    Arguments:
        phrase: the phrase to preprocess
    Returns:
        A list of tokens"""
    return list(itertools.filterfalse(lambda i: i in stop_words or i in punctuation, [i.lower() for i in word_tokenize(phrase)]))

def flatten(sl):
    return [j for i in sl for j in i]

# Ottieni la frase dopo il preprocessing (rimuove stopwords, punteggiatura, suddivide in token, li converte in minuscolo)
tokenized_courage = flatten(list(data.Courage.map(lambda x: preprocess_phrase(x))))
tokenized_paper = flatten(list(data.Paper.map(lambda x: preprocess_phrase(x))))
tokenized_apprehension = flatten(list(data.Apprehension.map(lambda x: preprocess_phrase(x))))
tokenized_sharpener = flatten(list(data.Sharpener.map(lambda x: preprocess_phrase(x))))

courage_freqs = utils.word_frequencies(tokenized_courage)
paper_freqs = utils.word_frequencies(tokenized_paper)
apprehension_freqs = utils.word_frequencies(tokenized_apprehension)
sharpener_freqs = utils.word_frequencies(tokenized_sharpener)

# Dati due sostantivi appartenenti ad una definizione (ordinati per frequenza e saltando i synset inesistenti)
# Trova il l'iperonimo comune più vicino
# Il termine di definizione che si cerca appartiene alla chiusura data dalla relazione di iponimia sull'iperonimo comune più vicino
def dumb_search(terms):
    """
    Arguments:
        terms: wordnet synsets for a concept definition
    Returns:
        a list of hyponyms deriving from the lowest common hypernym between the first 2 words
    """
    print(f"first term: {terms[0]}")
    print(f"second term: {terms[1]}")
    print(f"lowest common hypernyms: {terms[0].lowest_common_hypernyms(terms[1])}")
    return terms[0].lowest_common_hypernyms(terms[1])[0].closure(lambda i: i.hyponyms())

# Partendo dalle parole frequenti nelle definizioni, cerca su wordnet un sostantivo ad esso associato
# Filtra gli eventuali elementi vuoti (inesistenti in wordnet, come 'something')
# Prendi solo il primo synset (tra tutti quelli esistenti per una certa parola).
courage_nouns = [i[0] for i in list(filter(lambda i: i != [], [wn.synsets(i[0], wn.NOUN) for i in utils.word_frequencies(tokenized_courage)]))]
paper_nouns = [i[0] for i in list(filter(lambda i: i != [], [wn.synsets(i[0], wn.NOUN) for i in utils.word_frequencies(tokenized_paper)]))]
apprehension_nouns = [i[0] for i in list(filter(lambda i: i != [], [wn.synsets(i[0], wn.NOUN) for i in utils.word_frequencies(tokenized_apprehension)]))]
sharpener_nouns = [i[0] for i in list(filter(lambda i: i != [], [wn.synsets(i[0], wn.NOUN) for i in utils.word_frequencies(tokenized_sharpener)]))]

# Il termine cercato si trova tra gli iponimi?
print(wn.synsets('courage')[0] in dumb_search(courage_nouns)) # True
print(wn.synsets('paper')[0] in dumb_search(paper_nouns)) # True
print(wn.synsets('apprehension')[0] in dumb_search(apprehension_nouns)) # True
print(wn.synsets('sharpener')[0] in dumb_search(sharpener_nouns)) # True