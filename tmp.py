from bs4 import BeautifulSoup
import httpx

response = httpx.get('https://www.almbrand.dk')
soup = BeautifulSoup(response, 'html.parser')

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

print(title_text)