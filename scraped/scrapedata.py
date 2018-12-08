import requests
from bs4 import BeautifulSoup

def getdata(tags, filterby):
    if filterby == "off":
        url = "https://medium.com/tag/" + tags
        res = requests.get(url, "lxml")
        res.raise_for_status()
        soup = BeautifulSoup(res.text)
        #print(len(soup.select('time')))
        data = {
            'relatedTags' : [{'tag': a.get_text(), 'link': a.attrs.get('href', '')} for a in soup.select('a[data-action-source=related]')],
            'authors' : [a.get_text() for a in soup.select('div > a.u-accentColor--textDarken')],
            'titles' : [t.get_text() for t in soup.select('.graf--title')],
            'subtitles' : [t.get_text() for t in soup.select('.graf--trailing')],
            'coverImageUrl' : [t.attrs.get('src', '') for k in soup.select('.graf--figure') for t in k.descendants if t.has_attr('src')],
            'date' : [t.get_text() for t in soup.select('time')],
            'readingTime' : [t.attrs.get('title', '') for t in soup.select('.readingTime')],
            'responses' : [t.get_text() for t in soup.select('div.buttonSet.u-floatRight > .button--chromeless.u-baseColor--buttonNormal') if t.get_text()!=''],
            'claps' : [t.get_text() for t in soup.select('.js-multirecommendCountButton')]
        }
        return(data)
    else:
        url = "https://medium.com/tag/" + tags + "/latest"
        return(data)

print(getdata("business", "off"))