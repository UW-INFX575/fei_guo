
# coding: utf-8

# In[94]:

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk import stem
import re
from nltk.util import ngrams

#save all text file titles to one place
seq = ['6334220.txt','6334221.txt','6334222.txt','6334223.txt','6334224.txt','6334225.txt','6334226.txt','6334227.txt','6334228.txt','6334229.txt']


def clean_data(text_loc):
    stopset = set(stopwords.words('english')) #make stop words
    exclude = set(string.punctuation) #save punctuations

    #load text file and remove stop words, punctuation, and random letters
    with open(text_loc, 'r') as text_file:
        text = text_file.read()
        tokens = word_tokenize(str(text))
        tokens = [w for w in tokens if not w in stopset]
        tokens = [w for w in tokens if not w in exclude]  #http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        tokens = [w for w in tokens if len(w)>2] #http://stackoverflow.com/questions/24332025/remove-words-of-length-less-than-4-from-string

    #stemming the texts http://www.laurii.info/2012/08/simple-stemming-python/
    stemmed = []
    stemmer = stem.snowball.EnglishStemmer()

    for tag in tokens: #stem and change from unicode to str
        stemmed.append(unicodedata.normalize('NFKD', stemmer.stem(tag)).encode('ascii','ignore'))
    
    return stemmed

#Extract n-grams (unigrams, bigrams and trigrams)
#http://stackoverflow.com/questions/13423919/computing-n-grams-using-python
def ngrams(input, n):
    dic = {}
    for i in range(len(input)-n+1):
        g = ' '.join(input[i:i+n])
        dic.setdefault(g, 0)
        dic[g] += 1
    return dic


# In[122]:

# 3. Remove stop words from document (find your own stop-word list)
# 4. Stem words (using any stemming library)

file1 = clean_data(seq[0])
file2 = clean_data(seq[1])
file3 = clean_data(seq[2])
file4 = clean_data(seq[3])
file5 = clean_data(seq[4])
file6 = clean_data(seq[5])
file7 = clean_data(seq[6])
file8 = clean_data(seq[7])
file9 = clean_data(seq[8])
file10 = clean_data(seq[9])

#make a big text file with text from 10 txt files
#http://stackoverflow.com/questions/13613336/python-concatenate-text-files
with open('alltext.txt', 'w') as outfile:
    for fname in seq:
        with open(fname) as infile:
            outfile.write(infile.read())

file_all = clean_data('alltext.txt')


# In[138]:

# 5. Extract n-grams (unigrams, bigrams and trigrams)
# 6. Count the frequency of the n-grams for all ten documents and 
# for each individual document (10 documents).

# A. File with summary counts of unigrams for all 10 files combined. For example,
unigrams_all = ngrams(file_all, 1)

#http://stackoverflow.com/questions/11026959/python-writing-dict-to-txt-file-and-reading-dict-from-txt-file
import json 
json.dump(unigrams_all, open("A.txt",'w'))

# B. File with summary counts for bigrams for all 10 files combined. For example,
bigrams_all = ngrams(file_all, 2)
json.dump(bigrams_all, open("B.txt",'w'))

# C. File with summary counts for trigrams for all 10 files combined. For example,
trigrams_all = ngrams(file_all, 3)
json.dump(trigrams_all, open("C.txt",'w'))

# D. File with summary counts of unigrams for each of the 10 files. Same as above but for each individual file.
json.dump(ngrams(file1, 1), open("D1.txt",'w'))
json.dump(ngrams(file2, 1), open("D2.txt",'w'))
json.dump(ngrams(file3, 1), open("D3.txt",'w'))
json.dump(ngrams(file4, 1), open("D4.txt",'w'))
json.dump(ngrams(file5, 1), open("D5.txt",'w'))
json.dump(ngrams(file6, 1), open("D6.txt",'w'))
json.dump(ngrams(file7, 1), open("D7.txt",'w'))
json.dump(ngrams(file8, 1), open("D8.txt",'w'))
json.dump(ngrams(file9, 1), open("D9.txt",'w'))
json.dump(ngrams(file10, 1), open("D10.txt",'w'))

# E. File with summary counts of bigrams for each of the 10 files. Same as above but for each individual file.
json.dump(ngrams(file1, 2), open("E1.txt",'w'))
json.dump(ngrams(file2, 2), open("E2.txt",'w'))
json.dump(ngrams(file3, 2), open("E3.txt",'w'))
json.dump(ngrams(file4, 2), open("E4.txt",'w'))
json.dump(ngrams(file5, 2), open("E5.txt",'w'))
json.dump(ngrams(file6, 2), open("E6.txt",'w'))
json.dump(ngrams(file7, 2), open("E7.txt",'w'))
json.dump(ngrams(file8, 2), open("E8.txt",'w'))
json.dump(ngrams(file9, 2), open("E9.txt",'w'))
json.dump(ngrams(file10, 2), open("E10.txt",'w'))

# F. File with summary counts of trigrams for each of the ten files. Same as above but for each individual file.
json.dump(ngrams(file1, 3), open("F1.txt",'w'))
json.dump(ngrams(file2, 3), open("F2.txt",'w'))
json.dump(ngrams(file3, 3), open("F3.txt",'w'))
json.dump(ngrams(file4, 3), open("F4.txt",'w'))
json.dump(ngrams(file5, 3), open("F5.txt",'w'))
json.dump(ngrams(file6, 3), open("F6.txt",'w'))
json.dump(ngrams(file7, 3), open("F7.txt",'w'))
json.dump(ngrams(file8, 3), open("F8.txt",'w'))
json.dump(ngrams(file9, 3), open("F9.txt",'w'))
json.dump(ngrams(file10, 3), open("F10.txt",'w'))


