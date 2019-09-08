#cites articles from abc news site in apa style
import requests
import re
from bs4 import BeautifulSoup

url = input('Input the url to cite: ')
page = requests.get(url)
soup = BeautifulSoup(str(page.text), 'html.parser')

#div with some article info in it
byline = soup.find(class_='byline')

#find author
#this regex matches the url of the author's page
#example /news/simone-smale/12924081
author = re.search(r'/news/[a-z]+-[a-z]+/\d+',str(byline))
if author:
    author = re.search(r'[a-z]+-[a-z]+',author.group(0))
    author = author.group(0).split('-')

#format nicely
if author:
    #do last name
    nice_auth = author[1][0].upper()+author[1][1:]
    #add first initial
    nice_auth += ', '+author[0][0].upper()+'. '
else:
    nice_auth = 'N/A. '

#find date
time_line = soup.find(class_='timestamp')
#this regex matches the abc date string format
date = re.search(r'\w+ \d\d, \d\d\d\d',str(time_line))

#format nicely
if date:
    date = date.group(0)
    #get year
    nice_date = '('+date[-4:]+', '
    #do the month and day
    m_d = re.match(r'\w+ \d\d',date).group(0).split()
    month = m_d[0]
    day = m_d[1][1] if m_d[1][0] == '0' else m_d[1]
    nice_date += m_d[0]+' '+day+'). '
else:
    nice_date = '(N/A). '

#find title and paper
title_tag = soup.find('title').contents[0]
#split into title and paper name
title_tag = re.split(r' [-|] ',title_tag)
if len(title_tag) != 1:
    title = str(title_tag[0]+'. ')
    paper = '*'+title_tag[1]+'*. ' 
else:
    title = 'N/A. '
    paper = '*'+title+'*'

#format 'retrieved from'
retr = 'Retrieved from '+url

#put citation together
citation = '**'+nice_auth+nice_date+title+paper+retr+'**'

#print the final citation
print(citation)
