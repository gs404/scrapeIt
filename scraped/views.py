from django.shortcuts import render
from django.http import JsonResponse
from . import scrapedata

# Create your views here.
def scrape(request):
    return render(request, 'scraped/index.html')

def scraped(request):
    if not request.session.get('history', False):
        request.session['history'] = [request.POST["tags"]]
    else:
        sessionList = request.session['history']
        sessionList.append(request.POST["tags"])
        request.session['history'] = sessionList
    print(request.session['history'])
    data = scrapedata.getdata(request.POST["tags"], request.POST["selValue"])
    print(data)
    return JsonResponse(data)

def scrapeArticle(request):
    content, responses = scrapedata.getarticle(request.POST["alink"])
    data = {
        'content' : content,
        'responses' : responses
    }
    print(data)
    return JsonResponse(data, safe = False)