import os
import logging
import itertools

import numpy as np
import gensim

from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]

news_dump_file = 'corpus.dmp'
wiki_dump_file = 'wiki_corpus.dmp'

def iter_dump(dump_file):
    with open(dump_file, 'r', encoding='utf-8', errors='ignore') as dump:
        for text in dump:
            tokens = tokenize(text)
            if len(tokens) < 20:
                continue
            yield tokens

print('Creating doc_stream')
doc_stream = [tokens for tokens in iter_dump(news_dump_file)]
doc_stream += [tokens for tokens in iter_dump(wiki_dump_file)]

print('Creating Dictionary')
id2word = gensim.corpora.Dictionary(doc_stream)

print('Filtering extremes')
id2word.filter_extremes(no_below=20, no_above=0.2)

#if not os.path.exists('./data/bow.mm'):
print('Creating BOW')
bow = [id2word.doc2bow(tokens) for tokens in iter_dump(news_dump_file)]
bow += [id2word.doc2bow(tokens) for tokens in iter_dump(wiki_dump_file)]

print('Saving BOW')
gensim.corpora.MmCorpus.serialize('./data/bow.mm', bow, id2word)

print('Loading BOW')
mm_corpus = gensim.corpora.MmCorpus('./data/bow.mm')

print('Training LDA model')
lda_model = gensim.models.LdaModel(mm_corpus, num_topics=11, id2word=id2word, passes=5) #, alpha='asymmetric'

print('Print Topics')
lda_model.print_topics(-1)

print('Creating TF-IDF')
tfidf_model = gensim.models.TfidfModel(mm_corpus, id2word=id2word)

print('Creating lsi-model')
lsi_model = gensim.models.LsiModel(tfidf_model[mm_corpus], id2word=id2word, num_topics=200)

print('Save the models')
gensim.corpora.MmCorpus.serialize('./data/wiki_tfidf.mm', tfidf_model[mm_corpus])
gensim.corpora.MmCorpus.serialize('./data/wiki_lsa.mm', lsi_model[tfidf_model[mm_corpus]])
gensim.corpora.MmCorpus.serialize('./data/wiki_lda.mm', lda_model[mm_corpus])

print('Loading models')
tfidf_corpus = gensim.corpora.MmCorpus('./data/wiki_tfidf.mm')
# `tfidf_corpus` is now exactly the same as `tfidf_model[wiki_corpus]`
print(tfidf_corpus)

lsi_corpus = gensim.corpora.MmCorpus('./data/wiki_lsa.mm')
# and `lsi_corpus` now equals `lsi_model[tfidf_model[wiki_corpus]]` = `lsi_model[tfidf_corpus]`
print(lsi_corpus)

print('Done')