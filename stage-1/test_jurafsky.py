#!/usr/bin/env python3

"""
    This tests out the Dothraki grammar with cky
"""

from prettyprint import *
from cky import *
import nltk
import time

inputdata = [
    "book the flight through Houston",
    "does she prefer a morning flight",
    "I include this meal on that flight", # should work
    "she morning Houston book", # should fail
    "Houston prefer that Houston book morning", # should fail
    "morning he stewart ki dothraki" # should fail
    ]

parser = nltk.ChartParser(jurafsky_grammar)

for i in inputdata:
    tokens = nltk.word_tokenize(i)
    print(header(f"INPUT: {i}"))
    print(header(f"TOKENIZED: {tokens}"))
    #trees = parser.parse_all(tokens)
    #debug_trace(trees)
    a = time.time()
    table = cky_parse(tokens, jurafsky_grammar)
    print(table)
    debug_trace(table[0, len(tokens)])
    if (table[0, len(tokens)] != set()):
        print(success(bold("PARSING SUCCESSFUL")))
    else:
        print(fail(bold("PARSING FAILED")))
    b = time.time()
    print(info(f"TIME: {b-a} seconds"))
    print()
