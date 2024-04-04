import httpx
from bs4 import BeautifulSoup
from wiktionaryparser import WiktionaryParser
from nltk.corpus import wordnet as wn

URL = 'https://www.stengaardkirke.dk'

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
        tmp = wn.synsets(w, lang='dan')[0].pos()
        if tmp == 'n' and w not in filter:
            skribbl.append(w)
    except:
        pass

parser = WiktionaryParser()
parser.set_default_language('danish')

for w in skribbl:
    try:
        print(f"{w} is a {parser.fetch(w)[0]['definitions'][0]['partOfSpeech']}")
    except:
        pass
    

        