import short_url

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext as _

from . forms import UrlShortenerForm
from . models import UrlShortener, DELTA_DAYS


def urlshortener(request):
    # test message :)
    #messages.add_message(request, messages.ERROR,
                                 #_('The URL you have inserted is not valid.'))
    urlsh = None
    if request.method == 'GET':
        form = UrlShortenerForm()

    elif request.method == 'POST':
        form = UrlShortenerForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR,
                                 _('The URL you have inserted is not valid.'))
        else:
            entry = dict(original_url=form.cleaned_data['url'],
                         user_id=request.user if request.user.is_authenticated else None)
            
            urlsh = UrlShortener.objects.create(**entry)
            urlsh.shorten_url = short_url.encode_url(urlsh.pk)
            urlsh.save()
    
    context = dict(
        project_name='Url Shortener',
        form = form,
        delta_days = DELTA_DAYS,
        urlsh = urlsh
    )
    return render(request, 'urlshortener.html', context)
