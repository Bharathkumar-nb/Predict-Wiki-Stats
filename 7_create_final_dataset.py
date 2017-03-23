import os
import logging
import itertools
import json

import numpy as np
import gensim


from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

dump_folder = './Dumps'

semi_final_dataset_file = dump_folder + '/' + 'semi_final_dataset.dmp'
final_dataset_file = 'final_dataset.csv'


print('Loading models')
print()
print('Loading LDA Model')
lda_model = gensim.models.LdaModel.load('./data/lda_model.lda')
print('Loading LSI Model')
lsi_model = gensim.models.LsiModel.load('./data/lsi_model.lsi')
print('Loading Tfidf Model')
tfidf_model = gensim.models.TfidfModel.load('./data/tfidf_model.tfidf')

# print('Loading models with BOW')

# print('Loading tfidf_corpus')
# tfidf_corpus = gensim.corpora.MmCorpus('./data/tfidf.mm')
# # tfidf_corpus is now exactly the same as tfidf_model[wiki_corpus]
# print(tfidf_corpus)

# print('Loading lsi_corpus')
# lsi_corpus = gensim.corpora.MmCorpus('./data/lsa.mm')
# # and lsi_corpus now equals lsi_model[tfidf_model[wiki_corpus]] = lsi_model[tfidf_corpus]
# print(lsi_corpus)

# print('Loading lda_corpus')
# lda_corpus = gensim.corpora.MmCorpus('./data/lda.mm')
# # and lsi_corpus now equals lda_model[wiki_corpus]
# lda_corpus = np.array([lda_corpus]).transpose()

# X = np.hstack((lda_corpus[::2],lda_corpus[1::2]))

# print(X.shape)


def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]

id2word = gensim.corpora.Dictionary.load('./data/id2word.dic')


data = []
with open(semi_final_dataset_file, 'r', encoding='UTF-8') as semi_final_dataset:
    for row in semi_final_dataset:
        row = json.loads(row)
        
        # LDA
        # news_projection = lda_model[id2word.doc2bow(tokenize(row['news']))]
        # print(news_projection)
        # print(len(news_projection))

        # news_vector = [0]*11 # for LDA
        # for x,y in news_projection:
        #     news_vector[x] = y
        # wiki_projection = lda_model[id2word.doc2bow(tokenize(row['wiki']))]
        # wiki_vector = [0]*11
        # for x,y in wiki_projection:
        #     wiki_vector[x] = y

        # LSI
        news_projection = lsi_model[id2word.doc2bow(tokenize(row['news']))]
        news_vector = [y for x,y in news_projection]
        #print(len(news_vector))
        

        wiki_projection = lsi_model[id2word.doc2bow(tokenize(row['wiki']))]
        wiki_vector = [y for x,y in wiki_projection]
        #print(len(wiki_vector))
        #break
        y = int(row['views'])
        #data.append(news_vector + wiki_vector + [y])
        #data.append([x+y for x,y in zip(news_vector,wiki_vector)] + [y])
        data.append([x*y for x,y in zip(news_vector,wiki_vector)] + [y])

print(len(data))
print(data[:2])
        
data = np.array(data)
#data = np.array([data])
print(data.shape)

#np.savetxt('./final_dataset.csv',data, delimiter=",")
#np.savetxt('./final_dataset_addition.csv',data, delimiter=",")
#np.savetxt('./final_dataset_mult.csv',data, delimiter=",")
np.savetxt('./final_dataset_lsi.csv',data, delimiter=",")