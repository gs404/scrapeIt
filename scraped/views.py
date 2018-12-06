from django.shortcuts import render

# Create your views here.
def scrape(request):
    return render(request, 'scraped/index.html')
