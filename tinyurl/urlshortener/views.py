import copy
import short_url

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _

from . captcha import get_captcha
from . forms import UrlShortenerForm
from . models import UrlShortener, DELTA_DAYS


def _clean_expired_urls():
    urls = UrlShortener.objects.all()
    to_clean_up = []
    for url in urls:
        if url.is_expired():
            to_clean_up.append(url.pk)
    urls_to_clean = UrlShortener.objects.filter(pk__in=to_clean_up)
    urls_to_clean.delete()


def urlshortener(request):
    # test message :)
    #messages.add_message(request, messages.ERROR,
                                 #_('The URL you have inserted is not valid.'))
    urlsh = None
    captcha, captcha_img, captcha_hidden = get_captcha()
    initial={'captcha_hidden': captcha_hidden}

    if request.method == 'GET':
        form = UrlShortenerForm(initial=initial)
    elif request.method == 'POST':
        # clean oldies
        _clean_expired_urls()
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
                urlsh.shorten_url = short_url.encode_url(urlsh.pk)
                urlsh.save()
    
    context = dict(
        project_name='Url Shortener',
        form = form,
        delta_days = DELTA_DAYS,
        urlsh = urlsh,
        captcha_img = captcha_img,
        fqdn = getattr(settings, 'FQDN', request.build_absolute_uri())
    )
    return render(request, 'urlshortener.html', context)


def get_shorturl(request, shorturl):
    ursh = get_object_or_404(UrlShortener, shorten_url=shorturl)
    if ursh.is_expired():
        messages.add_message(request, messages.ERROR,
                                 _("L'Url da te inserito risulta essere scaduto e non più disponibile."))
    return HttpResponseRedirect(ursh.original_url)
    
    
    
