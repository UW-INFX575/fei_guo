
# coding: utf-8

# In[2]:

import lda
import lda.datasets
from __future__ import division, print_function
import numpy as np


# In[65]:

# LDA for the 10 documents provided by Jevin

#http://stackoverflow.com/questions/15899861/efficient-term-document-matrix-with-nltk
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer 

def fn_tdm_df(docs, xColNames = None, **kwargs):
    ''' create a term document matrix as pandas DataFrame
    with **kwargs you can pass arguments of CountVectorizer
    if xColNames is given the dataframe gets columns Names'''

    #initialize the  vectorizer
    vectorizer = CountVectorizer(**kwargs)
    x1 = vectorizer.fit_transform(docs)
    #create dataFrame
    df = pd.DataFrame(x1.toarray().transpose(), index = vectorizer.get_feature_names())
    if xColNames is not None:
        df.columns = xColNames

    return df


# In[66]:

DIR = '/Users/feismacbookpro/Desktop/INFX575/HW3/docs/'

def fn_CorpusFromDIR(xDIR):
    ''' functions to create corpus from a Directories
    Input: Directory
    Output: A dictionary with 
             Names of files ['ColNames']
             the text in corpus ['docs']'''
    import os
    Res = dict(docs = [open(os.path.join(xDIR,f)).read() for f in os.listdir(xDIR)],
               ColNames = map(lambda x: x[0:], os.listdir(xDIR)))
    return Res


# In[67]:

d1 = fn_tdm_df(docs = fn_CorpusFromDIR(DIR)['docs'],
          xColNames = fn_CorpusFromDIR(DIR)['ColNames'], 
          stop_words='english', charset_error = 'replace')  


# In[68]:

d1 = d1.T
d1


# In[69]:

#file locations
seq = ['6334220.txt','6334221.txt','6334222.txt','6334223.txt','6334224.txt','6334225.txt','6334226.txt','6334227.txt','6334228.txt','6334229.txt']

#function to load text
def load_data(text_loc):
    #load text file and remove stop words, punctuation, and random letters
    with open(DIR + text_loc, 'r') as text_file:
        text = text_file.read()
    return text

#make texts into one file
text = []
for i in range(len(seq)):
    text.append(load_data(seq[i]))


# In[70]:

#make vocab
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize

def make_vocab(text_loc):
    stopset = set(stopwords.words('english')) #make stop words
    exclude = set(string.punctuation) #save punctuations

    #load text file and remove stop words, punctuation, and random letters
    with open(text_loc, 'r') as text_file:
        text = text_file.read()
        tokens = word_tokenize(str(text))
        tokens = [w for w in tokens if not w in stopset]
        tokens = [w for w in tokens if not w in exclude]  #http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        tokens = [w for w in tokens if len(w)>2] #http://stackoverflow.com/questions/24332025/remove-words-of-length-less-than-4-from-string
        tokens = list(set(tokens))
    return tokens

vocab = make_vocab('/Users/feismacbookpro/Desktop/INFX575/HW2/alltext.txt')


# In[71]:

# document-term matrix
#http://chrisstrelioff.ws/sandbox/2014/11/13/getting_started_with_latent_dirichlet_allocation_in_python.html
# X = lda.datasets.load_reuters()
X = np.array(d1)
print("type(X): {}".format(type(X)))
print("shape: {}\n".format(X.shape))

# vocab = lda.datasets.load_reuters_vocab()
print("type(vocab): {}".format(type(vocab)))
print("len(vocab): {}\n".format(len(vocab)))

# # titles for each story
# titles = lda.datasets.load_reuters_titles()
titles = text
print("type(titles): {}".format(type(titles)))
print("len(titles): {}\n".format(len(titles)))


# In[72]:

doc_id = 3
word_id = 1

print("doc id: {} word id: {}".format(doc_id, word_id))
print("-- count: {}".format(X[doc_id, word_id]))
print("-- word : {}".format(vocab[word_id]))
print("-- doc  : {}".format(titles[doc_id]))


# In[73]:

model = lda.LDA(n_topics=5, n_iter=500, random_state=1)
model.fit(X)

topic_word = model.topic_word_
print("type(topic_word): {}".format(type(topic_word)))
print("shape: {}".format(topic_word.shape))


# In[74]:

for n in range(5):
    sum_pr = sum(topic_word[n,:])
    print("topic: {} sum: {}".format(n, sum_pr))


# In[75]:

n = 5
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))


# In[53]:

# Discover Culture Holes among 2 groups of toy documents

# make text for each group
toyDIR = '/Users/feismacbookpro/Desktop/INFX575/HW3/toy/'
locs = ['doc1.txt', 'doc2.txt', 'doc3.txt', 'doc4.txt', 'doc5.txt']

# group1 is doc1 and doc2
group1 = []
t = open(toyDIR + locs[0])
for word in t.read().split():
    group1.append(word)

t = open(toyDIR + locs[1])
for word in t.read().split():
    group1.append(word)

# group2 is doc3 to doc5
group2 = []
t = open(toyDIR + locs[2])
for word in t.read().split():
    group2.append(word)

t = open(toyDIR + locs[3])
for word in t.read().split():
    group2.append(word)
    
t = open(toyDIR + locs[4])
for word in t.read().split():
    group2.append(word)


# In[62]:

from collections import Counter
import math

# for H_x for each document
# entrophy = []
# for i in range(len(toy['docs'])):
#     count = Counter(toy['docs'][i].split())
#     vocab = list(set(toy['docs'][i].split()))
#     H_x = 0
#     for word in vocab:
#         p_x = count[word]/len(vocab)
#         if p_x > 0:
#             H_x += - p_x * math.log(p_x, 2)
#     entrophy.append(H_x)
# entrophy

# for H_x for each group
def shannon(group):
    entrophy = []
    count = Counter(group)
    vocab = list(set(group))
    H_x = 0
    for word in vocab:
        p_x = count[word]/len(vocab)
        if p_x > 0:
            H_x += - p_x * math.log(p_x, 2)
    entrophy.append(H_x)
    return entrophy

H1 = shannon(group1)
H2 = shannon(group2)

# for Q(pi||pj)

# for corpus code book S
text_all = []
for loc in locs:
    f = open(toyDIR + loc)
    for word in f.read().split():
        text_all.append(word)
text_all

# function to calculate Q(pi||pj)
def q_entrophy(text_all, group1, group2):
    count1 = Counter(group1)
    vocab1 = list(set(group1))
    count2 = Counter(group2)
    vocab2 = list(set(group2))
    s_count = Counter(text_all)
    s_vocab = list(set(text_all))
    q = 0
    for w in vocab1:
        p_1 = count1[w]/len(vocab1)
        p_2 = count2[w]/len(vocab2)
        s_x = s_count[w]/len(s_vocab)
        p_s1 = 0.9 * p_1 + 0.1 * s_x
        p_s2 = 0.9 * p_2 + 0.1 * s_x
        q += - p_s1 * math.log(p_s2, 2)
    return q

q_ij = q_entrophy(text_all, group1, group2)
q_ji = q_entrophy(text_all, group2, group1)

q_ij, q_ji


# In[60]:

H1, H2


# In[63]:

E_ij = H1[0] / q_ij
E_ji = H2[0] / q_ji

E_ij, E_ji


# In[64]:

C_ij = 1 - E_ij
C_ji = 1 - E_ji

C_ij, C_ji


# In[76]:

# try LDA on the toy set

d2 = fn_tdm_df(docs = fn_CorpusFromDIR(toyDIR)['docs'],
          xColNames = fn_CorpusFromDIR(toyDIR)['ColNames'], 
          stop_words='english', charset_error = 'replace')
d2 = d2.T
d2


# In[81]:

toyVocab = list(set(text_all))

X = np.array(d2)
model = lda.LDA(n_topics=2, n_iter=500, random_state=1)
model.fit(X)

topic_word = model.topic_word_


# In[82]:

n = 5
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(toyVocab)[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

