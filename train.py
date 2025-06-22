import requests
from bs4 import BeautifulSoup
from indic_transliteration.sanscript import transliterate, SchemeMap, SCHEMES
from indic_transliteration.sanscript import ITRANS, SINHALA


def get_wikipedia_politicians():
    url = "https://en.wikipedia.org/wiki/Category:Sri_Lankan_politicians"
    names = []
    while url and len(names) < 1000:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for li in soup.select('#mw-pages li'):
            names.append(li.get_text())
            if len(names) >= 1000:
                break
        more = soup.find('a', text='next page')
        url = 'https://en.wikipedia.org' + more['href'] if more else None
    return names

def translit_to_sinhala(names):
    sinhala_names = []
    for n in names:
        si = transliterate(n, sanscript.ITRANS, sanscript.SINHALA)
        sinhala_names.append(si)
    return sinhala_names

english = get_wikipedia_politicians()
sinhala_names = translit_to_sinhala(english)
with open('sri_lanka_politicians_si.txt', 'w', encoding='utf-8') as f:
    for name in sinhala_names:
        f.write(name + '\n')
