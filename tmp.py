import httpx
from bs4 import BeautifulSoup
from rich import print

ord = ['læs', 'efterår', 'ro', 'dukke', 'bog', 'arbejde', 'spørgsmål', 'kor', 'mulighed', 'under', 'begravelse', 'år', 'menneske', 'kirke', 'gang', 'valg', 'spiller', 'masse', 'lejlighed', 'kalender', 'række', 'medlemskab', 'selv', 'brug', 'kvinde', 'får', 'erklæring', 'kontakt', 'tak', 'forbindelse', 'forår', 'liv', 'gå', 'svar', 'musik', 'arbejder', 'solstråle', 'tid', 'historie', 'klasse', 'velkommen']

ord2 = []
def get_pos(ord):
    res = {}
    for w in ord:
        url = 'https://search.dsn.dk/api/?source=ro&size=1&from=0&search={}'
        content = httpx.get(url.format(w)).json()['hits']['hits'][0]['_source']
        rod = content['headword']
        soup = BeautifulSoup(content['html'], 'html.parser')
        pos = soup.find('abbr').text
        res.update(**{rod: pos})
    return [w for w, sb in res.items() if sb == 'sb.']

ord2 = get_pos([])

print(ord)
print(ord2)