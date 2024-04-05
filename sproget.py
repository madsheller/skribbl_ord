import httpx
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from tqdm import tqdm

import os

class skribbl:
    def __init__(self):
        self.words = []
        self.name = None
        self.destination = os.getcwd()
        self.filter = ['skal']
        self.lang = 'dan'

    def add_to_filter(self, words):
        self.filter = self.filter + words

    def parse_wn(self, words, lang):
        skribbl = []

        # list comprehenssion slower
        for w in set(words):
            try:
                tmp = wn.synsets(w, lang=self.lang)[0].pos()
                if tmp == 'n' and w not in filter:
                    skribbl.append(w)
            except:
                pass
        return skribbl

    def parse_dns(self, words):
        res = {}
        url = 'https://search.dsn.dk/api/?source=ro&size=1&from=0&search={}'
        for word in words:
            html = httpx.get(url.format(word)).json()
            content = html['hits']['hits'][0]['_source']
            rod = content['headword']
            soup = BeautifulSoup(content['html'], 'html.parser')
            pos = soup.find('abbr').text
            res.update(**{rod: pos})
        return [w for w, sb in res.items() if sb == 'sb.']

    def word_data(self, url, fast=False):
        html = httpx.get(url)

        soup = BeautifulSoup(html, 'html.parser')

        text = soup.get_text()
        words = text.split()

        rem = ['.', ',', '(', ')', '!', '…', '?', '"', "'", ';', '/', ':', '-', ' ']
        words = [w.translate((str.maketrans('','', ''.join(rem)))).lower() for w in words]

        nouns = self.parse_wn(words)
        
        if fast:
            return nouns
        else:
            return self.parse_dns(nouns)

    def get_name(self):
        pass

    def fetch(self, url, fast):
        return self.word_data(url, fast=fast)
    
    def get_results(self):
        return list(set(self.words))
    
    def to_txt(self):
        pass

    def to_csv(self):
        pass

# from typing import 

def is_noun(word):
    try:        
        url = 'https://search.dsn.dk/api/?source=ro&size=1&from=0&search={}'
        content = httpx.get(url.format('senge')).json()
        content = content['hits']['hits'][0]['_source']
        rod = content['headword']

        soup = BeautifulSoup(content['html'], 'html.parser')
        pos = soup.find('abbr').text

        return rod, pos=='sb.'
    except:
        url = 'https://ordnet.dk/ddo/ordbog?query={}'
        html = httpx.get(url.format(word))
        soup = BeautifulSoup(html, 'html.parser')
        contents = soup.find(class_='tekstmedium allow-glossing')
        return word, contents.text.split(',')[0] == 'substantiv'

def fine_sort(ord):
    res = {}
    for w in tqdm(ord):
        url = 'https://search.dsn.dk/api/?source=ro&size=1&from=0&search={}'
        content = httpx.get(url.format(w)).json()['hits']['hits'][0]['_source']
        rod = content['headword']
        soup = BeautifulSoup(content['html'], 'html.parser')
        pos = soup.find('abbr').text
        res.update(**{rod: pos})
    return [w for w, sb in res.items() if sb == 'sb.']

def skribbl(URL: str,
            fine: bool=True,
            lang: str='dan'):
    """
    Returns all nouns present on the URL page. 

    URL: url to scrape
    method: If True the function will look up all the detected nouns on Ordnet remove words that was faulty detected as nouns by WordNet. This greatly enhances the quality of the nouns at the cost of computational speed and possible IP bans. 
    filter: Words to not consider
    
    """

    html = httpx.get(URL)

    soup = BeautifulSoup(html, 'html.parser')

    text = soup.get_text()
    words = text.split()

    rem = ['.', ',', '(', ')', '!', '…', '?', '"', "'", ';', '/', ':', '-', ' ']
    words = [w.translate((str.maketrans('','', ''.join(rem)))).lower() for w in words]

    filter = ['skal']

    skribbl = []

    # list comprehenssion slower
    for w in set(words):
        try:
            tmp = wn.synsets(w, lang=lang)[0].pos()
            if tmp == 'n' and w not in filter:
                skribbl.append(w)
        except:
            pass

    if fine:
        skribbl = fine_sort(skribbl)

    return skribbl




