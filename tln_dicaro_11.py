#!/usr/bin/env python3 

import math
import itertools
import functools
import pandas as pd
import common.utils as utils
from nltk.tokenize import word_tokenize

definitions = "./resources/defs.csv"
data = pd.read_csv(definitions)

# Parameter that controls in how many phrases should a word appear, before not being considered a stopword
# Coherent results are with values >= 3
stopwords_treshold = 3

def definition_similarity(def1, def2):
    a = set(utils.preprocess_phrase(def1))
    b = set(utils.preprocess_phrase(def2))
    return len(a.intersection(b))/((len(a) + len(b)) * .5)

def flatten(sl):
    return [j for i in sl for j in i]

# Ottieni la frase dopo il preprocessing (rimuove stopwords, punteggiatura, suddivide in token, li converte in minuscolo e ne fa lo stemming)
tokenized_courage = flatten(list(data.Courage.map(lambda x: utils.preprocess_phrase(x))))
tokenized_paper = flatten(list(data.Paper.map(lambda x: utils.preprocess_phrase(x))))
tokenized_apprehension = flatten(list(data.Apprehension.map(lambda x: utils.preprocess_phrase(x))))
tokenized_sharpener = flatten(list(data.Sharpener.map(lambda x: utils.preprocess_phrase(x))))

# Ottieni il risultato della rimozione di stopwords (inglesi, di nltk) e della punteggiatura, dalle liste di token delle rispettive parole
courage_set = list(set(tokenized_courage))
paper_set = list(set(tokenized_paper))
apprehension_set = list(set(tokenized_apprehension))
sharpener_set = list(set(tokenized_sharpener))

courage_freqs = dict([(word, tokenized_courage.count(word)) for word in courage_set if tokenized_courage.count(word) > stopwords_treshold])
paper_freqs = dict([(word, tokenized_paper.count(word)) for word in paper_set if tokenized_paper.count(word) > stopwords_treshold])
apprehension_freqs = dict([(word, tokenized_apprehension.count(word)) for word in apprehension_set if tokenized_apprehension.count(word) > stopwords_treshold])
sharpener_freqs = dict([(word, tokenized_sharpener.count(word)) for word in sharpener_set if tokenized_sharpener.count(word) > stopwords_treshold])

# Mostra le frequenze delle parole, in ordine discendente
print(list(reversed(sorted([(word, tokenized_courage.count(word)) for word in courage_set if tokenized_courage.count(word) > stopwords_treshold], key = lambda x: x[1]))))
print(list(reversed(sorted([(word, tokenized_paper.count(word)) for word in paper_set if tokenized_paper.count(word) > stopwords_treshold], key = lambda x: x[1]))))
print(list(reversed(sorted([(word, tokenized_apprehension.count(word)) for word in apprehension_set if tokenized_apprehension.count(word) > stopwords_treshold], key = lambda x: x[1]))))
print(list(reversed(sorted([(word, tokenized_sharpener.count(word)) for word in sharpener_set if tokenized_sharpener.count(word) > stopwords_treshold], key = lambda x: x[1]))))

# Calcola il denominatore comune come la somma delle frequenze su tutte le parole
denominator = sum(courage_freqs.values()) + sum(paper_freqs.values()) + sum(apprehension_freqs.values()) + sum(sharpener_freqs.values())

# Calcola la similarità delle parole come la somma delle frequenze delle frasi per una certa parola, sulle frequenze totali di tutte le parole
courage_sim = sum(courage_freqs.values())/denominator
paper_sim = sum(paper_freqs.values())/denominator
apprehension_sim = sum(apprehension_freqs.values())/denominator
sharpener_sim = sum(sharpener_freqs.values())/denominator

print()
print()

# Mostra i risultati
print("Courage similarity: ", courage_sim)
print("Paper similarity: ", paper_sim)
print("Apprehension similarity: ", apprehension_sim)
print("Sharpener similarity: ", sharpener_sim)
print()
print("Percentage sum: ", courage_sim + paper_sim + apprehension_sim + sharpener_sim)
