from bs4 import BeautifulSoup
import re
from requests_futures.sessions import FuturesSession
import dill


def parse_speakers_and_quotes(page, year):
    """
    Extracts names of every person involved with the debate and 
    collects all of their quotes in a list.
    
    :param page: html page
    
    :returns dict: {speaker name: [quotes]}
    """
    #print year
    # fixes a BeautifulSoup problem that results in improper parsing
    page_soup = BeautifulSoup(page.text.encode('utf-8'))
    
    speaker_dict = dict()

    prev_speaker = ''
    for i in page_soup.find_all('p'):

        try: # search for name of person speaking
            curr_speaker = re.findall('[A-Z]+:', i.text)[0].strip(':')
            prev_speaker = curr_speaker
            quote = re.split(':', i.text)[1]

        except IndexError: # if name not in line
            quote = i.text

        if prev_speaker+'_'+year not in speaker_dict:
            # add speaker to speaker_dict with list of quotes as value
            speaker_dict[prev_speaker+'_'+year] = [quote]
        else:
            # append quote to speaker's list of quotes
            speaker_dict[prev_speaker+'_'+year].append(quote)
            
    return speaker_dict


if __name__ == '__main__':
    
    transcript_urls = [] # read urls from file
    with open('../txt/debate_links.txt', 'rb') as infile:
        for line in infile.readlines():
            transcript_urls.append(line)

    npages = len(transcript_urls) # for testing

    session = FuturesSession(max_workers=5)
    futures = [session.get(url[0]) for url in transcript_urls[:npages]]

    dates = [url[1] for url in transcript_urls[:npages]]
    results = zip(futures, dates)

    debate_transcripts = [parse_speakers_and_quotes(future.result(), date) for future, date in results]

    # dump it to a dill file so we don't need to blast UCSB's servers again
    dill.dump(debate_transcripts, open('../dills/debate_transcripts_list.dill', 'wb'))
