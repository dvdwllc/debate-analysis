from bs4 import BeautifulSoup
import requests
import re
from requests_futures.sessions import FuturesSession
import dill


def parse_speakers_and_quotes(page):
    """
    Extracts names of every person involved with the debate and 
    collects all of their quotes in a list.
    
    :param page: html page
    
    :returns dict: {speaker name: [quotes]}
    """
    
    # start at appropriate spot in page
    start = page.text.index('<span class="displaytext">')
    page_soup = BeautifulSoup(page.text[start:])
    
    speaker_dict = dict()

    prev_speaker = None
    for i in page_soup.find_all('p'):

        try: # search for name of person speaking
            curr_speaker = re.findall('[A-Z]+:', i.text)[0]
            prev_speaker = curr_speaker
            quote = re.split(':', i.text)[1]

        except IndexError: # if name not in line
            quote = i.text

        if prev_speaker not in speaker_dict:
            # add speaker to speaker_dict with list of quotes as value
            speaker_dict[prev_speaker] = [quote]
        else:
            # append quote to speaker's list of quotes
            speaker_dict[prev_speaker].append(quote)
    return speaker_dict


# fast way to scrape shit (sorry, UCSB)
session = FuturesSession(max_workers=5)
futures = [session.get(url) for url in transcript_urls]


# list of all debate transcripts!
debate_transcripts = [parse_speakers_and_quotes(future.result()) for future in futures]

# dump it to a dill file so we don't need to blast UCSB's servers again
dill.dump(debate_transcripts, open('debate_transcripts_list.dill', 'wb'))