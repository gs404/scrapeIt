from django.conf.urls import url
from . import views

app_name = 'scraped'

urlpatterns = [
    url(r'^$', views.scrape, name="scrape"),
]