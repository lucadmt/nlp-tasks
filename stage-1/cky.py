#!/usr/bin/env python3

"""
    This is a python3 implementation of the CKY algorithm.
"""

from prettyprint import info, bold, success, fail
import numpy as np
import argparse
import nltk
import time

parser = argparse.ArgumentParser(description='Test CKY parser')
parser.add_argument("-t", "--show-trace", required=False, help='Show debug trace during execution')
args = parser.parse_args()

debug_enable = args.show_trace

np.set_printoptions(linewidth=100)

jurafsky_grammar = nltk.data.load('./resources/jurafsky_grammar_cnf.cfg')
dothraki_grammar = nltk.data.load('./resources/dothraki_grammar.cfg')

def debug_trace(dstring):
    if debug_enable:
        print(dstring)

def heads_for_string(grammar, string):
    debug_trace(f"SEARCHING HEAD FOR STRING: '{string}'")
    result = set()
    #print(list(zip(grammar.productions(), range(len(grammar.productions())))))
    for i in list(zip(grammar.productions(), range(len(grammar.productions())))):
        p_rhs = i[0].rhs()
        if (string != None and len(string) > 0) and (p_rhs[0] == string):
            result.add((i[1], i[0].lhs()))
    return result

# Searches within 'grammar' a production.
def heads_for_production(grammar, rhs):
    debug_trace(f"P: SEARCHING HEAD FOR {rhs}")
    result = set()
    #print(list(zip(grammar.productions(), range(len(grammar.productions())))))
    for i in list(zip(grammar.productions(), range(len(grammar.productions())))):
        p_rhs = i[0].rhs()
        if (p_rhs[0] == rhs[0][1] and p_rhs[1] == rhs[1][1]):
            result.add((i[1], i[0].lhs()))
    debug_trace(f"FOUND: {result}")
    return result

def heads_for_productions(grammar, prod_rhs):
    if (prod_rhs[0] == set() or prod_rhs[1] == set()) or (prod_rhs[0] == None or prod_rhs[1] == None):
        # there's no production to try (must be in CNF)
        debug_trace(info(prod_rhs))
        debug_trace(info(bold("SKIPPING SEARCH: ONE OF THE SET OF SYMBOLS IS EMPTY (VIOLATES CNF)")))
        return set()
    sym_set1 = list(prod_rhs[0])
    sym_set2 = list(prod_rhs[1])
    result = set()
    combos = set()
    for i in sym_set1:
        for j in sym_set2:
            if i[1] != j[1]: # If it's equal, it violates CNF
                combos.add((i, j))
    for i in combos:
        result = result.union(heads_for_production(grammar, i))
    return result


def cky_parse(words, grammar):
    table = np.empty((len(words)+1, len(words)+1), dtype=object)
    for j in range(1, len(words)+1):
        # take all the *heads* in the grammar, which produce words[j]
        heads = heads_for_string(grammar, words[j-1])
        table[j-1, j] = set(heads)
        debug_trace(info(f"Filling {j-1},{j} with: {heads}"))
        # implements a decrementing loop (step=-1)
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                debug_trace(bold(info("j,i,k: {}.{}.{}".format(j, i, k))))
                if  (table[i, j] == None):
                    table[i, j] = heads_for_productions(grammar, (table[i, k], table[k, j]))
                else:
                    table[i, j] = table[i,j].union(heads_for_productions(grammar, (table[i, k], table[k, j])))
    debug_trace(info(bold("RESULT: {}".format(table[0, len(words)]))))
    return table