
# coding: utf-8

# In[54]:

import lda
import lda.datasets
from __future__ import division, print_function
import numpy as np
import string
from nltk.tokenize import word_tokenize
from collections import defaultdict
import unicodedata
from collections import Counter
import math


# In[62]:

#function to load abstracts and cleaning them, make them into list of words,
#and put them in groups according to the group file
def load_data(DIR, groupfile, abstractfile):
    # import groups.txt
    group = [line.strip() for line in open(DIR + groupfile)]
    group.pop(0)

    groups = {} #make groups into a dictionary {pid:group#}
    for row in group:
        row = row.split('\t')
        groups[row[0]] = row[1] 

    # import abstracts and remove the rows with null, seperate key and value
    abstract = [line.strip() for line in open(DIR + abstractfile)]
    abstracts = []
    for row in abstract:
        row = row.split('\t')
        if row[1] != 'null':
            abstracts.append(row)
    abstracts.pop(0) #pop the column names

    #make a new dictionary of abstracts stopwords removed then with pids as keys
    abstracts_new = {}
    for i in range(len(abstracts)):
        abstracts_new[abstracts[i][0]] = rmStopWords(abstracts[i][1])

    # allocate paragraphs into groups by the groups dictionary
    group = defaultdict(list)
    for i in range(len(abstracts_new.keys())):
        key = groups[abstracts_new.keys()[i]]
        for word in abstracts_new.values()[i]:
            group[key].append(unicodedata.normalize('NFKD', word).encode('ascii','ignore'))

    # remove column names for group
    group.pop('0', None)
    
    return group


# In[57]:

#function to remove stop words from a paragraph is texts, return list of words
def rmStopWords(text_paragraph):
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
    
    stopset = set(stopwords) #make stop words
    exclude = set(string.punctuation) #save punctuations

    #load text file and remove stop words
    tokens = word_tokenize(str(text_paragraph).decode('utf-8'))
    tokens = [w for w in tokens if not w in exclude]
    tokens = [w.lower() for w in tokens if not w.lower() in stopset]
    tokens = [w for w in tokens if len(w)>2]
    tokens = list(tokens)
    return tokens

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
    count1 = Counter(group1) #word count for group1
    vocab1 = list(set(group1)) #vocab for gourp1
    
    count2 = Counter(group2) #word count for group2
    vocab2 = list(set(group2)) #vocab for gourp2
    
    s_count = Counter(text_all) #count for text_all
    s_vocab = list(set(text_all)) #vocab for text_all
    
    sum1 = sum(count1.itervalues()) #sum of total counts for group1
    sum2 = sum(count2.itervalues()) #sum of total counts for group2
    s_sum = sum(s_count.itervalues()) #sum of total counts for text_all
    
    q = 0
    for w in vocab1: #for each word in group1 vocab
        p_1 = count1[w]/sum1
        p_2 = count2[w]/sum2
        s_x = s_count[w]/s_sum
        p_s1 = 0.99 * p_1 + 0.01 * s_x
        p_s2 = 0.99 * p_2 + 0.01 * s_x
        q += - p_s1 * math.log(p_s2, 2)
    return q

# function to calculate the culture hole
def JD(H1, group1, group2):
    text_all  = group1 + group2 #make a corpus which combines 2 groups
    q_ij = q_entropy(text_all, group1, group2) #calculate q entropy
    E_ij = H1[0] / q_ij
    C_ij = 1 - E_ij
#     return format(C_ij, ".15g")
    return C_ij


# In[58]:

def jargan_distance(C, group, length):
    for i in range(length):
        H1 = shannon(group[str(i+1)])
        for j in range(length):
            C[i][j] = JD(H1, group[str(i+1)],group[str(j+1)])
    return C

def calculateJD(DIR, groupfile, abstractfile):
    group = load_data(DIR, groupfile, abstractfile)
    length = len(group)
    C = [[0 for x in range(length)] for x in range(length)] 
    C = jargan_distance(C, group, length)
    return C


# In[61]:

#results for the large set
from matplotlib.pyplot import show
import cProfile

#file locations
DIR = '/Users/feismacbookpro/Desktop/INFX575/HW3/big/'
groupfile = 'groups2.txt'
abstractfile = 'abstracts2.txt'

import cProfile
cProfile.run( 'calculateJD(DIR, groupfile, abstractfile)' )

# C = calculateJD(DIR, groupfile, abstractfile)

# Z = linkage(C)
# dendo = dendrogram(Z)

# import json

# with open('/Users/feismacbookpro/Desktop/INFX575/HW3/big/dendo.jason', 'w') as f:
#     json.dump(dendo, f)
# # show()


# In[60]:

#results for the small test set 

#file locations
DIR = '/Users/feismacbookpro/Desktop/INFX575/HW3/final/'
groupfile = 'group1.txt'
abstractfile = 'abstract1.txt'

import cProfile
cProfile.run( 'calculateJD(DIR, groupfile, abstractfile)' )

C_final = calculateJD(DIR, groupfile, abstractfile)
# C_final

group = load_data(DIR, groupfile, abstractfile)
group

#calculating the q for trouble shooting
length = len(group)
H1 = []
Q = [[0 for x in range(length)] for x in range(length)]
for i in range(length):
#     H1.append(shannon(group[str(i+1)]))
    for j in range(length):
        group1 = group[str(i+1)]
        group2 = group[str(j+1)] 
        text_all  = group1 + group2
        Q[i][j] = q_entropy(text_all, group1, group2)
#             C[i][j] = JD(H1, group[str(i+1)],group[str(j+1)])
Q


# In[40]:

from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage

Z = linkage(C_final)
# dendrogram(Z)
Z

