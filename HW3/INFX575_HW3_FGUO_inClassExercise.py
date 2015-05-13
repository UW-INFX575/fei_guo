
# coding: utf-8

# In[1]:

import lda
import lda.datasets
from __future__ import division, print_function
import numpy as np


# In[97]:

#file locations
DIR = '/Users/feismacbookpro/Desktop/INFX575/HW3/test/'

# import groups.txt
group = [line.strip() for line in open(DIR + 'groups.txt')]
group.pop(0)

groups = {}
for row in group:
    row = row.split('\t')
    groups[row[0]] = row[1]
groups


# In[159]:

# import abstracts and remove the rows with null
abstract = [line.strip() for line in open(DIR + 'abstracts.txt')]
abstracts = []
for row in abstract:
    row = row.split('\t')
    if row[1] != 'null':
        abstracts.append(row)
abstracts


# In[167]:

# make a corpus with all texts from all paragraphs
text = []
for row in abstracts:
    text.append(row[1])
text_all = " ".join(text)


# In[53]:

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


# In[168]:

import string
from nltk.tokenize import word_tokenize

def rmStopWords(text_paragraph):
    stopset = set(stopwords) #make stop words

    #load text file and remove stop words, punctuation, and random letters
    tokens = word_tokenize(str(text_paragraph))
    tokens = [w for w in tokens if not w in stopset]
    tokens = list(tokens)
    return tokens

# remove stoprwords from all the paragraphs
rm_stopWords = []
for row in text:
    rm_stopWords.append(rmStopWords(row))
# len(rm_stopWords)

rm_sw_textALL = rmStopWords(text_all)
len(rm_sw_textALL)
#total words: 1686


# In[160]:

# combine the pid with the paragraphs that have stop words removed in to a dictionary
pid = []
for i in range(len(abstracts)):
    pid.append(abstracts[i][0])

abstracts_new = {}
for i in range(len(pid)):
    abstracts_new[pid[i]] = rm_stopWords[i]


# In[156]:

# allocate paragraphs into groups by the groups dictionary
group1 = []
group2 = []
group3 = []
for i in range(len(abstracts_new.keys())):
    if groups[abstracts_new.keys()[i]] == '1':
        for word in abstracts_new.values()[i]:
            group1.append(word)
    if groups[abstracts_new.keys()[i]] == '2':
        for word in abstracts_new.values()[i]:
            group2.append(word)
    if groups[abstracts_new.keys()[i]] == '3':
        for word in abstracts_new.values()[i]:
            group3.append(word)


# In[182]:

from collections import Counter
import math

# for H_x for each group
def shannon(group):
    entrophy = []
    count = Counter(group)
    vocab = list(set(group))
    H_x = 0
    for word in vocab:
#         p_x = count[word]/len(group)
        p_x = count[word]/sum(count.itervalues())
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
    q = 0
    for w in vocab1:
        p_1 = count1[w]/sum(count1.itervalues())
        p_2 = count2[w]/sum(count2.itervalues())
        s_x = s_count[w]/sum(s_count.itervalues())
        p_s1 = 0.99 * p_1 + 0.01 * s_x
        p_s2 = 0.99 * p_2 + 0.01 * s_x
        q += - p_s1 * math.log(p_s2, 2)
    return q

# function to calculate the culture hole
def JD(text_all, group1, group2):
    H1 = shannon(group1) #calculate shannon entropy
    text_all  = group1 + group2 #make a corpus which combines 2 groups
    q_ij = q_entropy(text_all, group1, group2) #calculate q entropy
    E_ij = H1[0] / q_ij
    C_ij = 1 - E_ij
    return C_ij


# In[180]:

# culture hole from group 1 to 2 and 3
C_12 = JD(rm_sw_textALL, group1, group2)
C_13 = JD(rm_sw_textALL, group1, group3)

# culture hole from group 2 to 1 and 3
C_21 = JD(rm_sw_textALL, group2, group1)
C_23 = JD(rm_sw_textALL, group2, group3)

# culture hole from group 3 to 1 and 2
C_31 = JD(rm_sw_textALL, group3, group1)
C_32 = JD(rm_sw_textALL, group3, group2)


# In[181]:

C_12, C_13, C_21, C_23, C_31, C_32

