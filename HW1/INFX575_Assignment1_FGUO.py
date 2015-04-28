
# coding: utf-8

# In[2]:

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, HTTPError, URLError
from time import sleep # be nice
import re
import os
import unicodedata
import numpy as np


# In[135]:

#reference: https://www.snip2code.com/Snippet/297497/Some-code-that-works-for-me-----(JournoC

def make_soup(url):
    req = Request(url, headers ={'User-Agent':'Chrome'})
    try:
        html = urlopen(req).read()
        return BeautifulSoup(html, "lxml")
    except (URLError, HTTPError) as e:
#         print e.fp.read()
        print "Error"

# Generate a list of all the links to each faculty, the faculty's name and the name of the department
def get_faculty_links(section_url):
    soup = make_soup(section_url)
    
    title = soup.title.text #get title for department and university
    title = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
    text = title.split(",")
    department = " ".join(text[0].split("-")[1].split())
    university = " ".join(text[1].split())
    
    faculty_links = [] #list for links to each faculty
    fnames = [] #list for first names
    lnames = [] #list for last namesdegree,
    
    td = soup.findAll("td", { "class":"people-list-name" })
    for i in range(len(td)):  #for each td tag
        last = td[i].find('strong').text  #last name are in the strong tags
        #first names are in the a tags excluding the strong tags
        first = ''.join(text for text in td[i].a.find_all(text=True) if text.parent.name != "strong")
        #decode unicode data
        lnames.append(unicodedata.normalize('NFKD', last).encode('ascii','ignore'))
        fnames.append(unicodedata.normalize('NFKD', first).encode('ascii','ignore'))
        #find the faculty_links for each faculty
        for a in td[i].find_all('a', href=True):
            faculty_links.append(a['href'])
            
    return fnames, lnames, faculty_links, department, university

# Get PhD information
def get_faculty_info(faculty_url):
    soup = make_soup(faculty_url)  #go into each faculty_link
    if (soup != None): 
        #find the div tag with profile-degrees
        div = soup.find("div", { "class":"profile-degrees" })
        if (div != None): #if there is a div tag with the class specified
            ul = div.find('ul').text  #find the degree info in the list
            degree = unicodedata.normalize('NFKD', ul).encode('ascii','ignore')
            PhD = get_phd(degree)
        else: #if there is no div with the specified class
            PhD = "Not on this page" #degree info is not on this page
    else: PhD = "Page not accessible" #if can not access soup, tell me
    return PhD

# text scrapy for phd info
def get_phd(degree):
    degree = re.sub(r'\d', "", degree) #take the year off
    if (re.search('Ph', degree, re.IGNORECASE) != None):  #if there is a "Ph"
        if (re.search('MIT', degree, re.IGNORECASE) != None): 
            PhD = "Massachusetts Institute of Technology" #fix MIT problem
        # if there are commas, split them and go through each part
        elif (len(degree.split(',')) > 1): 
            if (re.search('university', degree, re.IGNORECASE) != None) or (re.search('institute', degree, re.IGNORECASE) != None):
                for j in range(len(degree.split(','))): 
                    if (re.search('university', degree.split(',')[j], re.IGNORECASE) != None) or (re.search('institute', degree.split(',')[j], re.IGNORECASE) != None):
                        PhD = degree.split(',')[j] #take the part with keyword 'university' or 'institute'
            else: #if no keyword is there, clean up as much as possible
                ph = re.search('Ph', degree, re.IGNORECASE)
                end = ph.end()+2
                PhD = degree[end:]
                PhD = re.sub(r'\d', "", PhD) #take out the year
    else: #if there is no "Ph" in the text, take the whole thing just in case
        PhD = degree
    return PhD


# In[136]:

# extract name, faculty url, department and university from the directory website
url  = ("https://engineering.purdue.edu/ECE/People/Faculty")
fnames, lnames, faculty_links, department, university = get_faculty_links(url)


# In[5]:

# extract gradate school information from each faculty page
grad_school = [] # a list to faculty info
for i in range(len(faculty_links)): 
    faculty = faculty_links[i]
#     print i
    PhD = get_faculty_info(faculty).strip()
#     print PhD
    grad_school.append(PhD)
    #sleep(1) # be nice

# print grad_school


# In[137]:

# make department and school same length as the other columns
depart = []
school = []
for i in range(len(fnames)):
    depart.append(department)
    school.append(university)


# In[138]:

# put all lists together
faculty = fnames, lnames, grad_school, school, depart

# output to a csv file, results needs to be transposed as the list is by default verticalled stacked
import csv
with open("faculty_purdue.csv", "wb") as f:
    writer = csv.writer(f) 
    for row in faculty:
        writer.writerow(row)

