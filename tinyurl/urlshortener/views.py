import copy

from collections import OrderedDict
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django_form_builder.forms import BaseDynamicForm
from rest_framework import viewsets
from rest_framework import permissions

from . captcha import get_captcha
from . forms import UrlShortenerForm
from . models import UrlShortener, DELTA_DAYS
from . serializers import UrlShortenerSerializer, clean_expired_urls


_PROJECT_NAME = 'Url Shortener'

TINYURL_TEMPLATE = getattr(settings, 'TINYURL_TEMPLATE', 'urlshortner.html')

# this is the dictionary that builds the DynamicForm
constructor_dict = OrderedDict([
    # URLField
    # ('URL',
        # ('CustomURLField',
            # {'label': 'url',
             # 'required': True,
             # 'help_text': _('The URL that would be shortened'),
             # 'pre_text': '',
             # 'attrs': {'class': 'form-control'}
            # },
            # '')
    # ),
    # Captcha
    ('CaPTCHA',
        ('CustomCaptchaComplexField',
            {'label': 'CaPTCHA',
             'pre_text': '',
             # 'attrs': {'class': 'form-control'}
            },
            '')
    ),
])

def urlshortener(request):
    urlsh = None
    tinyurl = ''
    # captcha, captcha_img, captcha_hidden = get_captcha()
    url = dict(request.GET).get('url', '')

    initial={
             # 'captcha_hidden': captcha_hidden,
             'url': url[0] if url else ''}

    if request.method == 'GET':
        form = UrlShortenerForm(initial=initial)
        form_captcha = BaseDynamicForm.get_form(constructor_dict=constructor_dict)
    elif request.method == 'POST':
        # clean oldies
        clean_expired_urls()
        form = UrlShortenerForm(data=request.POST)
        form_captcha = BaseDynamicForm.get_form(constructor_dict=constructor_dict,
                                                data=request.POST)
        
        if not all((form.is_valid(), form_captcha.is_valid())):
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
        project_name=_PROJECT_NAME,
        form = form,
        form_captcha = form_captcha,
        delta_days = DELTA_DAYS,
        urlsh = urlsh,
        # captcha_img = captcha_img,
        tinyurl = tinyurl
    )
    return render(request, TINYURL_TEMPLATE, context)


def get_shorturl(request, shorturl):
    urlsh = get_object_or_404(UrlShortener, shorten_url=shorturl)
    landing_page = getattr(settings, 'TINYURL_REDIRECT_LANDINGPAGE', True)
    if landing_page:
        context = dict(
            project_name = _PROJECT_NAME,
            urlsh = urlsh,
            tinyurl = urlsh.get_redirect_url(request)
        )
        return render(request, 'urlshortener_redirect_landing.html', context)
    else:
        return HttpResponseRedirect(urlsh.original_url)


# API
class UrlShortenerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view and create shortened urls.
    """
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head']
