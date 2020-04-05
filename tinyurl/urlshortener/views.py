from django.shortcuts import render
from . forms import UrlShortenerForm


def urlshortener(request):
    context = dict(
        project_name='Url Shortener',
        form = UrlShortenerForm()
    )
    return render(request, 'urlshortener.html', context)
