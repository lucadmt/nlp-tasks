#!/usr/bin/env python3

"""
    This tests out the Dothraki semantic grammar
"""

from nltk import load_parser, word_tokenize
from prettyprint import *
import time

parser = load_parser('./resources/dothraki_grammar.fcfg', trace=0)

inputdata = [
    "hash yer astoe ki dothraki",
    "anha zhilak yera",
    "anha gavork",
    #"anha hash dothraki ki", # should fail
    #"zhilak yera hash", # should fail
    #"yer hash dothraki anha yera" # should fail
    ]
for i in inputdata:
	tokens = word_tokenize(i)
	print(header(f"INPUT: {i}"))
	print(header(f"TOKENIZED: {tokens}"))
	for tree in parser.parse(tokens):
		print(tree.label()['SEM'])