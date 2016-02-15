from bs4 import BeautifulSoup
import requests

# change this to the actual url and use requests to pull the page
index = "http://www.presidency.ucsb.edu/debates.php"
response = requests.get(index)

# beautiful soup object for html parsing
soup = BeautifulSoup(response.text.encode('utf-8'))

# find all links to debate transcripts
debate_links = soup.find_all('td', attrs={'class':'doctext'})
debate_dates = soup.find_all('td', attrs={'class':'docdate'})

# get urls for each transcript
transcript_urls = []
n_sans_link = 0
for i in range(len(debate_links)):
    try:
        transcript_urls.append(
            (debate_links[i].select('a')[0].get('href'), 
             debate_dates[i].text.split(', ')[1])
        )
    except IndexError:
        n_sans_link += 1
        
print 'got %i urls, %i listings with no link.' % (len(transcript_urls), n_sans_link)

outfile = 'debate_links.txt'
with open(outfile, 'wb') as out:
    for i in transcript_urls:
        out.write(i)
    print 'links written to %s' % outfile