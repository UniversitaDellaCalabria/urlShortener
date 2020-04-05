import short_url

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
            # recyple already forged tinyurls
            urlsh = UrlShortener.objects.filter(original_url=form.cleaned_data['url']).first()
            if not urlsh:
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


def get_shorturl(request, shorturl):
    ursh = get_object_or_404(UrlShortener, shorten_url=shorturl)
    if ursh.is_expired():
        messages.add_message(request, messages.ERROR,
                                 _('The URL you have inserted is Expired.'))
    return HttpResponseRedirect(ursh.original_url)
    
    
    
