from django.shortcuts import render
from django.http import JsonResponse
from . import scrapedata

# Create your views here.
def scrape(request):
    return render(request, 'scraped/index.html')

def scraped(request):
    data = scrapedata.getdata(request.POST["tags"], request.POST["selValue"])
    print(data)
    return JsonResponse(data)