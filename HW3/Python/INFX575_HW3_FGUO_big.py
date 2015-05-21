
# coding: utf-8

# In[3]:

import lda
import lda.datasets
from __future__ import division, print_function
import numpy as np


# In[4]:

#file locations
DIR = '/Users/feismacbookpro/Desktop/INFX575/HW3/big/'

# import groups.txt
group = [line.strip() for line in open(DIR + 'groups2.txt')]
group.pop(0)

groups = {}
for row in group:
    row = row.split('\t')
    groups[row[0]] = row[1]
# groups


# In[5]:

# import abstracts and remove the rows with null
abstract = [line.strip() for line in open(DIR + 'abstracts2.txt')]
abstracts = []
for row in abstract:
    row = row.split('\t')
    if row[1] != 'null':
        abstracts.append(row)
abstracts.pop(0)
# abstracts


# In[6]:

# make a corpus with all texts from all paragraphs
text = []
for row in abstracts:
    text.append(row[1])
text_all = " ".join(text)


# In[7]:

stopwords = ["all","just","being","over","both","through","yourselves","its",
             "before","herself","had","should","to","only","under","ours","has",
             "do","them","his","very","they","not","during","now","him","nor",
             "did","this","she","each","further","where","few","because","doing",
             "some","are","our","ourselves","out","what","for","while","does",
             "above","between","t","be","we","who","were","here","hers","by","on",
             "about","of","against","s","or","own","into","yourself","down","your",
             "from","her","their","there","been","whom","too","themselves","was",
             "until","more","himself","that","but","don","with","than","those",
             "he","me","myself","these","up","will","below","can","theirs","my",
             "and","then","is","am","it","an","as","itself","at","have","in","any",
             "if","again","no","when","same","how","other","which","you","after",
             "most","such","why","a","off","i","yours","so","the","having","once"]


# In[8]:

import string
from nltk.tokenize import word_tokenize

def rmStopWords(text_paragraph):
    stopset = set(stopwords) #make stop words
    exclude = set(string.punctuation) #save punctuations

    #load text file and remove stop words
    tokens = word_tokenize(str(text_paragraph).decode('utf-8'))
    tokens = [w for w in tokens if not w in exclude]
    tokens = [w.lower() for w in tokens if not w.lower() in stopset]
    tokens = [w for w in tokens if len(w)>2]
    tokens = list(tokens)
    return tokens

# remove stoprwords from all the paragraphs
rm_stopWords = []
for row in text:
    rm_stopWords.append(rmStopWords(row))
len(rm_stopWords)

# rm_sw_textALL = rmStopWords(text_all)
# len(rm_sw_textALL)
#total words: 1686


# In[9]:

# combine the pid with the paragraphs that have stop words removed in to a dictionary
pid = []
for i in range(len(abstracts)):
    pid.append(abstracts[i][0])

abstracts_new = {}
for i in range(len(pid)):
    abstracts_new[pid[i]] = rm_stopWords[i]


# In[10]:

from collections import defaultdict
import unicodedata

# allocate paragraphs into groups by the groups dictionary
group = defaultdict(list)
for i in range(len(abstracts_new.keys())):
    key = groups[abstracts_new.keys()[i]]
    for word in abstracts_new.values()[i]:
        group[key].append(unicodedata.normalize('NFKD', word).encode('ascii','ignore'))

# remove group 0
group.pop('0', None)


# In[16]:

from collections import Counter
import math

# for H_x for each group
def shannon(group):
    entrophy = []
    count = Counter(group)
    vocab = list(set(group))
    H_x = 0
    sum_count = sum(count.itervalues())
    for word in vocab:
        p_x = count[word]/sum_count
        if p_x > 0:
            H_x += - p_x * math.log(p_x, 2)
    entrophy.append(H_x)
    return entrophy

# for Q(pi||pj)

# function to calculate Q(pi||pj)
def q_entropy(text_all, group1, group2):
    count1 = Counter(group1)
    vocab1 = list(set(group1))
    count2 = Counter(group2)
    vocab2 = list(set(group2))
    s_count = Counter(text_all)
    s_vocab = list(set(text_all))
    sum1 = sum(count1.itervalues())
    sum2 = sum(count2.itervalues())
    s_sum = sum(s_count.itervalues())
    q = 0
    for w in vocab1:
        p_1 = count1[w]/sum1
        p_2 = count2[w]/sum2
        s_x = s_count[w]/s_sum
        p_s1 = 0.99 * p_1 + 0.01 * s_x
        p_s2 = 0.99 * p_2 + 0.01 * s_x
        q += - p_s1 * math.log(p_s2, 2)
    return q

# function to calculate the culture hole
def JD(H1, group1, group2):
#     H1 = shannon(group1) #calculate shannon entropy
    text_all  = group1 + group2 #make a corpus which combines 2 groups
    q_ij = q_entropy(text_all, group1, group2) #calculate q entropy
    E_ij = H1[0] / q_ij
    C_ij = 1 - E_ij
    return format(C_ij, ".15g")


# In[17]:

def jargan_distance(group):
    C = [[0 for x in range(10)] for x in range(10)] 
    for i in range(10):
        H1 = shannon(group[str(i+1)])
        for j in range(10):
            C[i][j] = JD(H1, group[str(i+1)],group[str(j+1)])
    return C

cProfile.run( 'jargan_distance(group)' )

