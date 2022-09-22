#!/usr/bin/python3

from nltk.corpus import wordnet as wn
import pandas as pd
import functools

property_norms = pd.read_csv('./resources/mcrae_pn.tsv', sep='\t')
concepts = set(property_norms.Concept)

def get_property_norms(concept):
    """
        Get property norms for the target concept
    """
    return list(property_norms[property_norms.Concept == concept].Feature)

def merge_concept(concept):
    """
        Get a definition for concept, that integrates property norms
    """
    synset = ""
    try:
        synset = wn.synsets(concept)[0]
    except IndexError:
        try:
            synset = wn.synsets(concept.split('_')[0])[0]
        except IndexError:
            return f"{concept} [NO-WORDNET-DEF]: "
    string = functools.reduce(lambda x, y: f"{x}, {y}", [i.replace('_', ' ').replace('beh - ', 'it ').replace('inbeh - ', 'it ') for i in get_property_norms(concept)])
    return f"{concept}: {synset.definition()}. {string}"

for concept in concepts:
    print(f"{merge_concept(concept)}.\n")