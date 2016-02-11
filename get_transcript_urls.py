from bs4 import BeautifulSoup

# change this to the actual url and use requests to pull the page
index = "sample_html/Presidential Debates.html"

# beautiful soup object for html parsing
soup = BeautifulSoup(open(index, 'r'))

# find all links to debate transcripts
debate_links = soup.find_all('td', attrs={'class':'doctext'})

# get urls for each transcript
transcript_urls = []
n_sans_link = 0
for i in debate_links:
    try:
        transcript_urls.append(i.select('a')[0].get('href'))
    except IndexError:
        n_sans_link += 1
        
print 'got %i urls, %i listings with no link.' % (len(transcript_urls), n_sans_links)