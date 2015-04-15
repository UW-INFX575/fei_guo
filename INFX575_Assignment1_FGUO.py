
# coding: utf-8

# In[2]:

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, HTTPError, URLError
from time import sleep # be nice
import re
import os
import unicodedata


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
    for i in range(len(td)): 
        lnames.append(td[i].find('strong'))
        fnames.append(td[i].a.text)
        for a in td[i].find_all('a', href=True):
            faculty_links.append(a['href'])
            
    return fnames, lnames, faculty_links, department, university

# Get PhD information
def get_faculty_info(faculty_url):
    soup = make_soup(faculty_url)
    if (soup != None):
        div = soup.find("div", { "class":"profile-degrees" })
        if (div == None):
            div_new = soup.find("div", { "class":"rule" }).text
            degree = unicodedata.normalize('NFKD', div).encode('ascii','ignore')
            PhD = get_phd(degree)
#             PhD = "Not on this page"
        else:
            ul = div.find('ul').text
            degree = unicodedata.normalize('NFKD', ul).encode('ascii','ignore')
            degree = re.sub(r'\d', "", degree)
            if (re.search('Ph', degree, re.IGNORECASE) != None): 
                if (re.search('MIT', degree, re.IGNORECASE) != None): 
                    PhD = "Massachusetts Institute of Technology"
                elif (len(degree.split(',')) > 1):
                    if (re.search('university', degree, re.IGNORECASE) != None) or (re.search('institute', degree, re.IGNORECASE) != None):
                        for j in range(len(degree.split(','))): 
                            if (re.search('university', degree.split(',')[j], re.IGNORECASE) != None) or (re.search('institute', degree.split(',')[j], re.IGNORECASE) != None):
                                PhD = degree.split(',')[j]
                    else:
                        ph = re.search('Ph', degree, re.IGNORECASE)
                        end = ph.end()+2
                        PhD = degree[end:]
                        PhD = re.sub(r'\d', "", PhD) #take out the year
            else:
                PhD = degree
    else: PhD = "Page not accessible"
    print PhD
    return PhD

def get_phd(degree):
    degree = re.sub(r'\d', "", degree)
    if (re.search('Ph', degree, re.IGNORECASE) != None): 
        if (re.search('MIT', degree, re.IGNORECASE) != None): 
            PhD = "Massachusetts Institute of Technology"
        elif (len(degree.split(',')) > 1):
            if (re.search('university', degree, re.IGNORECASE) != None) or (re.search('institute', degree, re.IGNORECASE) != None):
                for j in range(len(degree.split(','))): 
                    if (re.search('university', degree.split(',')[j], re.IGNORECASE) != None) or (re.search('institute', degree.split(',')[j], re.IGNORECASE) != None):
                        PhD = degree.split(',')[j]
            else:
                ph = re.search('Ph', degree, re.IGNORECASE)
                end = ph.end()+2
                PhD = degree[end:]
                PhD = re.sub(r'\d', "", PhD) #take out the year
    else:
        PhD = degree
    return "irregular page:" + PhD


# In[5]:

url  = ("https://engineering.purdue.edu/ECE/People/Faculty")
fnames, lnames, faculty_links, department, university = get_faculty_links(url)


# In[136]:

data = [] # a list to faculty info
for i in range(len(faculty_links)): 
    faculty = faculty_links[i]
    print i
    PhD = get_faculty_info(faculty).strip()
#     print PhD
    data.append(PhD)
    #sleep(1) # be nice

print data


# In[137]:

link = faculty_links[15]
print link
# soup = make_soup(link)

# print link
# div = soup.find("div", { "class":"profile-degrees" })
# print div == None
# # ul = div.find('ul').text
# # ul
# # #

# PhD = get_faculty_info(faculty_links[0])


# # PhD = re.sub('[\,]', "", PhD)
# # PhD = PhD.strip(',')
# print PhD

# print re.search('MIT', PhD, re.IGNORECASE) != None


# degree = unicodedata.normalize('NFKD', ul).encode('ascii','ignore')

# a = re.search('Ph', degree, re.IGNORECASE)
# a.group()
# end = a.end()+3
# len(degree)
# degree[end:].split(',')[0]

# if (soup.find("div", { "class":"profile-degrees" }) == None ):
#     PhD = "not on this page"
# else:
#     div = soup.find("div", { "class":"profile-degrees" }).text
#     print div
#     if (re.search(',', div) == None): 
#         PhD = div
#     else:
#         PhD = " ".join(div.split(',')[1].split(',')[0].split())



soup = make_soup(faculty_links[61])
if (soup != None):
    div = soup.find("div", { "class":"profile-degrees" })
    if (div == None ):
        PhD = "Not on this page"
    else:
        ul = div.find('ul').text
        degree = unicodedata.normalize('NFKD', ul).encode('ascii','ignore')  

        if (re.search('Ph', degree, re.IGNORECASE) != None): 
            if (re.search('MIT', degree, re.IGNORECASE) != None): 
                PhD = "Massachusetts Institute of Technology"
            
            elif (len(degree.split(',')) > 1):
                if (re.search('university', degree, re.IGNORECASE) != None) or (re.search('Institute', degree, re.IGNORECASE) != None):
                    for j in range(len(degree.split(','))): 
                        if (re.search('university', degree.split(',')[j], re.IGNORECASE) != None) or (re.search('institute', degree.split(',')[j], re.IGNORECASE) != None):
                            PhD = degree.split(',')[j]
                else:
                    ph = re.search('Ph', degree, re.IGNORECASE)
                    end = ph.end()+2
                    PhD = degree[end:]
                    PhD = re.sub(r'\d', "", PhD) #take out the year
        else:
            PhD = degree
else: PhD = "Page not accessible"
# print PhD

PhD

# print re.search('mit', PhD, re.IGNORECASE) != None
# print re.search('Ph', PhD, re.IGNORECASE) == True

