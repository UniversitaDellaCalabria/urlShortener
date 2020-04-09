import copy

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework import permissions

from . captcha import get_captcha
from . forms import UrlShortenerForm
from . models import UrlShortener, DELTA_DAYS
from . serializers import UrlShortenerSerializer, clean_expired_urls


def urlshortener(request):
    urlsh = None
    tinyurl = ''
    captcha, captcha_img, captcha_hidden = get_captcha()
    initial={'captcha_hidden': captcha_hidden}

    if request.method == 'GET':
        form = UrlShortenerForm(initial=initial)
    elif request.method == 'POST':
        # clean oldies
        clean_expired_urls()
        form = UrlShortenerForm(data=request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR,
                                 _('I valori da te inseriti non risultano validi.'))
            initial['url'] = form.data.get('url')
            form = UrlShortenerForm(initial=initial)
        else:
            # recyple already forged tinyurls
            urlsh = UrlShortener.objects.filter(original_url=form.cleaned_data['url']).first()
            if not urlsh:
                entry = dict(original_url=form.cleaned_data['url'],
                             user_id=request.user if request.user.is_authenticated else None)
                urlsh = UrlShortener.objects.create(**entry)
                urlsh.set_shorten_url()
            tinyurl = urlsh.get_redirect_url(request)
                
    context = dict(
        project_name='Url Shortener',
        form = form,
        delta_days = DELTA_DAYS,
        urlsh = urlsh,
        captcha_img = captcha_img,
        tinyurl = tinyurl
    )
    return render(request, 'urlshortener.html', context)


def get_shorturl(request, shorturl):
    urlsh = get_object_or_404(UrlShortener, shorten_url=shorturl)
    landing_page = getattr(settings, 'TINYURL_REDIRECT_LANDINGPAGE', True)
    if landing_page:
        context = dict(
            urlsh = urlsh,
            tinyurl = urlsh.get_redirect_url(request)
        )
        return render(request, 'urlshortener_redirect_landing.html', context)
    else:
        return HttpResponseRedirect(urlsh.original_url)
    
    
# API
class UrlShortenerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
    permission_classes = [permissions.IsAuthenticated]
