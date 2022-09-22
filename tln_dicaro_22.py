#!/usr/bin/env python3

import os
import pickle 
import tempfile
import pyLDAvis
import pandas as pd
import seaborn as sns
from pprint import pprint
from gensim import models
from gensim import corpora
import common.utils as utils
import matplotlib.pyplot as plt
from collections import defaultdict
import pyLDAvis.gensim_models as gensimvis

data = open('./resources/psy_corpus.txt', 'r').read()

documents = data.replace('\n\n\n', '').replace('\n', '').split('|---|')
print(f"Documents Number: {len(documents)}")

processed_corpus = list(filter(lambda x: x!=[], [utils.preprocess_phrase(doc) for doc in documents]))

def plot_difference(mdiff, title="", annotation=None):
    """Helper function to plot difference between models.

    Uses matplotlib as the backend."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(18, 14))
    data = ax.imshow(mdiff, cmap='RdBu_r', origin='lower')
    plt.title(title)
    plt.colorbar(data)

# remove words that appear only once
frequency = defaultdict(int)
for text in processed_corpus:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in processed_corpus
]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lda_model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=len(documents))
corpus_lda = lda_model[corpus_tfidf]

print(lda_model.print_topics(len(documents)))

mdiff, annotation = lda_model.diff(lda_model, distance='hellinger', num_words=50)
plot_difference(mdiff, title="Topic difference (one model)[hellinger distance]", annotation=annotation)
plt.show()

# Visualize the topics
# pyLDAvis.enable_notebook()
LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_'+str(len(documents)))

LDAvis_prepared = gensimvis.prepare(lda_model, corpus, dictionary)
with open(LDAvis_data_filepath, 'wb') as f:
    pickle.dump(LDAvis_prepared, f)

# load the pre-prepared pyLDAvis data from disk
with open(LDAvis_data_filepath, 'rb') as f:
    LDAvis_prepared = pickle.load(f)
pyLDAvis.save_html(LDAvis_prepared, './results/ldavis_prepared_'+ str(len(documents)) +'.html')
LDAvis_prepared