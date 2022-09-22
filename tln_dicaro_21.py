#!/usr/bin/env python3

import re
import nltk
import math
import common.utils as utils
import matplotlib.pyplot as plt
from statistics import stdev

# number of words in a phrase
w = 20
data = open('./resources/bpd_corpus.txt', 'r').read()

paragraphs = data.split('\n\n')
phrases = list(filter(lambda x: x != '', utils.flatten([paragraph.split('.') for paragraph in paragraphs])))

counts = []
for phrase in enumerate(phrases):
    counts.append((phrase[0], utils.preprocess_phrase(phrase[1].strip())))

counts_nostem = []
for phrase in enumerate(phrases):
    counts_nostem.append((phrase[0], utils.preprocess_phrase_nostem(phrase[1].strip())))

tokenized_text = utils.flatten(list(zip(*counts))[1])
tokenized_nostem = utils.flatten(list(zip(*counts_nostem))[1])


def vocaboulary_introduction(tokenized_text):
    """Measures the introduction of words in adjacent phrases in a text
    Arguments:
        tokenized_text: a list of lemmas from the original text
    Returns:
        A list of scores for each 'gap' (point between 2 adjacent phrases)"""
    scores = []
    seen = set()
    for i in range(1, len(tokenized_text)+1, (2*w)):
        seen_in_first = set(tokenized_text[int(i/4):int((i/2))]).difference(seen)
        seen_in_second = set(tokenized_text[int((i/2)):i]).difference(seen)
        seen.update(seen_in_first)
        seen.update(seen_in_second)
        #print(f"i: {i}\nin 1: {len(seen_in_first)}\nin2: {len(seen_in_second)}\nresult: {(len(seen_in_first) + len(seen_in_second)/ 2*w)}")
        scores.append((int(i/2), (len(seen_in_first) + len(seen_in_second))/ 2*w))
    return scores

def plot_smoothing(s, scores):
    """Smooths the scores to obtain a better curve to locate variations in the discourse
    Arguments:
        s: the window of scores to consider in the smoothing for a certain gap
        scores: list of tuples like (gap_number, score)
    Returns:
        A list of smoothed scores for each 'gap' (point between 2 adjacent phrases)"""
    smoothed_scores = []
    for g in range(0, len(scores)):
        if g >= s/2:
            scores_left = list(zip(*scores[g-int(s/2):g]))[1]
        else:
            if g == 0:
                scores_left = [0]
            else:
                scores_left = list(zip(*scores[:g]))[1]
        
        if g <= len(tokenized_text) - s/2:
            scores_right = list(zip(*scores[g:g+int(s/2)]))[1]
        else:
            scores_right = list(zip(*scores[g:]))[1]
        score = (scores[g][1] + sum(scores_left) + sum(scores_right))/(1+len(scores_right) + len(scores_left))
        smoothed_scores.append((scores[g][0], score))
    return smoothed_scores

def depth_score(scores):
    """Measures the depth in the scores for lexical similarity
    Arguments:
        scores: a list of lexical similarity measures
    Returns:
        A list of depth scores"""
    depth_scores = []
    for i in range(0, len(scores)):
        depth_scores.append((scores[i][0], (scores[i-1][1] - scores[i][1]) + (scores[(i+1)%len(scores)][1] - scores[i][1])))
    return depth_scores

scores = vocaboulary_introduction(tokenized_text)
plt.plot(list(zip(*scores))[1], label="Raw")
smoothed_scores = plot_smoothing(10, scores)
plt.plot(list(zip(*smoothed_scores))[1], label="Smoothed")
depth_scores = list(zip(*depth_score(scores)))
#plt.plot(depth_scores[1], label="Depth")
plt.legend()
plt.show()

def boundary_identifier(scores_pairs, denominator=1):
    scores = [s[1] for s in scores_pairs]
    std = stdev(scores)
    s_maxf = (0, scores[0])
    s_maxs = (0, scores[0])
    s_min = (0, scores[0])
    breakpoints = []
    found_min = False
    for i in zip(range(1, len(scores)), scores):

        # search first max
        # then search a min, lesser than first max at least std times
        # then search another max, which is bigger 'std' than min

        #print(f"first max: {s_maxf}; min: {s_min}; second max: {s_maxs}")

        if i[1] > s_maxf[1]:
            s_maxf = i
    
        if i[1] < s_min[1] - int(std/denominator):
            s_min = i
            found_min = True

        if i[1] > s_min[1] + int(std/denominator):
            s_maxs = i
            if found_min:
                breakpoints.append((s_min[0], s_min[1], scores_pairs[s_min[0]][0]))
                s_maxf = s_maxs
                s_min = s_maxs
                s_maxs = (0, 0)
                found_min = False
    return breakpoints

smoothed_scores_single = [x[1] for x in smoothed_scores]
breakpoints = boundary_identifier(smoothed_scores, denominator=2)
print(breakpoints)
x, y, words = tuple(zip(*breakpoints))
plt.plot(smoothed_scores_single)
#plt.plot(depth_scores)
for i in x:
    plt.axvline(i, color='red')
plt.show()

window = 3
for i in words:
    to_match = "(.*)"
    for j in tokenized_nostem[i-window:i+window]:
        to_match += f"{j}(.*)"
    #to_match+="$"
    print(to_match)
    regex = re.compile(to_match, re.M)
    match = regex.search(data.lower())
    try:
        print(match.group(0))
    except AttributeError:
        pass
    print()
