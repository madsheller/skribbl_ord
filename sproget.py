import httpx
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from tqdm import tqdm

import os
import csv

class skribbl:
    def __init__(self):
        self.words = []
        self.len = 0
        self.name = ''
        self.destination = os.getcwd()
        self.filter = ['skal']
        self.lang = 'dan'
        self.cached = None

    def add_to_filter(self, words):
        self.filter = self.filter + words

    def parse_wn(self, words):
        skribbl = []
        
        word_list = set(words)
        print(f'{len(word_list)} unique words.')

        # list comprehenssion slower
        for w in set(words):
            try:
                tmp = wn.synsets(w, lang=self.lang)[0].pos()
                if tmp == 'n' and w not in self.filter:
                    skribbl.append(w)
            except:
                pass
        return skribbl

    def parse_dns(self, words):
        res = {}
        url = 'https://search.dsn.dk/api/?source=ro&size=1&from=0&search={}'
        for word in tqdm(words):
            html = httpx.get(url.format(word)).json()
            content = html['hits']['hits'][0]['_source']
            rod = content['headword']
            soup = BeautifulSoup(content['html'], 'html.parser')
            pos = soup.find('abbr').text
            res.update(**{rod: pos})
        return [w for w, sb in res.items() if sb == 'sb.']

    def word_data(self, url, fast):
        html = httpx.get(url)

        soup = BeautifulSoup(html, 'html.parser')

        self.name = self.name + self.get_name(soup=soup)

        text = soup.get_text()
        words = text.split()

        rem = ['.', ',', '(', ')', '!', '…', '?', '"', "'", ';', '/', ':', '-', ' ']
        words = [w.translate((str.maketrans('','', ''.join(rem)))).lower() for w in words]
        print(f'Found {len(words)} on the website: {url}')
        
        nouns = self.parse_wn(words)

        if fast:
            print(f'There are {len(nouns)} nouns on the website.')
            return nouns
        else:
            print(f'There are {len(nouns)} nouns on the website.')
            return self.parse_dns(nouns)

    def get_name(self, soup):
        title_text = soup.title.text
        if '|' in title_text:
            title_text = title_text.split('|', 1)[1].strip()

        title_text = ''.join(title_text.split())
        print(title_text)

        d = {
            '.': '',
            'æ': 'ae',
            'ø': 'oe',
            'å': 'aa',
            }

        for old, new in d.items():
            title_text = title_text.replace(old, new)

        return title_text

    def fetch(self, url, fast=False):
        data = self.word_data(url, fast=fast)
        l = sum(len(i) for i in data)
        print(f'Fetch returned {len(data)} words containing {l} characters in total.')
        self.words = self.words + data
        self.len = sum(len(i) for i in self.words)
        print(f'The total number of words is now {len(self.words)}.')
        print(f'The total number of characters is now {self.len}.')

    def get_results(self):
        if len(self.words) < 10:
            print('Ikke tilstrækkelig mange ord i listen. Tilføj flere ord.')
        return list(set(self.words))

    def to_txt(self):
        output = ','.join(self.words)
        os.makedirs('output', exist_ok=True)
        with open(f'output/{self.name}.txt', 'w') as file:
            file.write(output)

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

def skribbl_old(URL: str,
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




