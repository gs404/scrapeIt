import requests
import json
from bs4 import BeautifulSoup
from .models import *
from django.shortcuts import get_object_or_404

def getdata(tags, filterby):
    if filterby == "off":
        url = "https://medium.com/tag/" + tags
    else:
        url = "https://medium.com/tag/" + tags + "/latest"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    
    data = {
        'relatedTags' : [{'tag': a.get_text(), 'link': a.attrs.get('href', '')} for a in soup.select('a[data-action-source=related]')],
        'authors' : [a.get_text() if a.get_text()!='' else '' for a in soup.select('div > a.u-accentColor--textDarken')],
        'titles' : [t.get_text() if t.get_text()!='' else 'None' for t in soup.select('.graf--title')],
        'subtitles' : [t.get_text() if t.get_text()!='' else 'None' for t in soup.select('.graf--trailing')],
        'links' : [l.attrs.get('href', '') for l in soup.select('a[data-action=open-post]')],
        'coverImageUrl' : [t.attrs.get('src', '') for k in soup.select('.graf--figure') for t in k.descendants if t.has_attr('src')],
        'date' : [t.get_text() if t.get_text()!='' else 'None' for t in soup.select('time')],
        'readingTime' : [t.attrs.get('title', '') for t in soup.select('.readingTime')],
        'responses' : [t.get_text() if t.get_text()!='' else 'None' for t in soup.select('div.buttonSet.u-floatRight > .button--chromeless.u-baseColor--buttonNormal') if t.get_text()!=''],
        'claps' : [t.get_text() if t.get_text()!='' else 'None' for t in soup.select('.js-multirecommendCountButton')]
    }

    tempset = []
    data['links'] = [tempset.append(x) for x in data['links'] if not x in tempset]
    data['links'] = tempset

    if data['authors']==[] and data['titles']==[]:
        data['found'] = False
        print('Could not find data for tag: ' + tags)
        print('Related tags: ')
        for i in data['relatedTags']:
            print(i['tag'])
        return(data)
    else:
        data['found'] = True
        t = Tag.objects.create(tag = tags)

    for i in list(zip(data['authors'], data['titles'], data['subtitles'], data['links'], data['coverImageUrl'], data['date'], data['readingTime'], data['responses'], data['claps'])):
        a = Article(tag = t, title = i[1], author = i[0], subtitle = i[2], cover = i[4], date = i[5], readingTime = i[6], claps = i[8], link = i[3])
        a.save()

    return(data)


def getarticle(alink):
    res = requests.get(alink)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        content = list(soup.select('.section-content')[0].children)[2].get_text()
    except:
        content = list(soup.select('.section-content')[0].children)[0].get_text()

    a = get_object_or_404(Article, link = alink)
    a.content = content
    a.save()

    articleId = soup.select('link[rel=canonical]')[0].attrs.get('href','').split('-')[-1]

    r = requests.get(
            url='https://medium.com/_/api/posts/' + articleId + '/responses?filter=best',
            headers={
                'X-Requested-With': 'XMLHttpRequest'
        }
    )
    
    response, by = [], []
    r = json.loads(r.text[16:])

    if r['payload']['value']!=[]:
        for i in r['payload']['value']:
            response.append(i['previewContent']['bodyModel']['paragraphs'][0]['text'])

        for i in r['payload']['references']['User'].values():
            if i['name']!=a.author:
                by.append(i['name'])
            else:
                continue
    
        for i in list(zip(by, response)):
            k = Response.objects.create(article = a, by = i[0], content = i[1])
    else:
        r = requests.get(
            url='https://medium.com/_/api/posts/' + articleId + '/responsesStream?filter=other',
            headers={
                'X-Requested-With': 'XMLHttpRequest'
            }
        )
        r = json.loads(r.text[16:])

        for i in r['payload']['references']['Post'].values():
            response.append(i['previewContent']['bodyModel']['paragraphs'][0]['text'])

        for i in r['payload']['references']['User'].values():
            if i['name']!=a.author:
                by.append(i['name'])
            else:
                continue

        for i in list(zip(by, response)):
            k = Response.objects.create(article = a, by = i[0], content = i[1])

    return(content, list(zip(by, response)))

# print(getdata("business", "off"))
# getarticle("https://medium.com/darius-foroux/how-to-be-a-leader-that-inspires-people-to-change-f9ea6ea06daf")