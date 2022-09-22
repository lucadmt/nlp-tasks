#!/usr/bin/env python3

"""
    This tests out the Dothraki grammar with cky
"""

from cky import *
from prettyprint import *
import nltk
import time

inputdata = [
    "hash yer astoe ki dothraki",
    "anha zhilak yera",
    "anha gavork",
    "anha hash dothraki ki", # should fail
    "zhilak yera hash", # should fail
    "yer hash dothraki anha yera" # should fail
    ]

parser = nltk.ChartParser(dothraki_grammar)

for i in inputdata:
    tokens = nltk.word_tokenize(i)
    print(header(f"INPUT: {i}"))
    print(header(f"TOKENIZED: {tokens}"))
    #trees = parser.parse_all(tokens)
    #debug_trace(trees)
    a = time.time()
    table = cky_parse(tokens, dothraki_grammar)
    print(table)
    debug_trace(table[0, len(tokens)])
    if (table[0, len(tokens)] != set()):
        print(success(bold("PARSING SUCCESSFUL")))
    else:
        print(fail(bold("PARSING FAILED")))
    b = time.time()
    print(info(f"TIME: {b-a} seconds"))
    print()
