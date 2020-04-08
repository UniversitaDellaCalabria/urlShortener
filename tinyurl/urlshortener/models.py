import logging
import short_url

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


DELTA_DAYS = getattr(settings, 'TINYURL_DURATION_DAYS', 0)
logger = logging.getLogger(__name__)


def clean_expired_urls():
    # if not DELTA_DAYS do nothing
    if not DELTA_DAYS:
        return
    
    urls = UrlShortener.objects.all()
    to_clean_up = []
    for url in urls:
        if (timezone.now() - url.created).days >= DELTA_DAYS:
            to_clean_up.append(url.pk)
    urls_to_clean = UrlShortener.objects.filter(pk__in=to_clean_up)
    urls_to_clean.delete()


class UrlShortener(models.Model):
    # it could be also anonymous 
    user_id = models.ForeignKey(get_user_model(),
                                on_delete=models.SET_NULL,
                                blank=True, null=True)
    original_url = models.URLField(max_length=2048)
    shorten_url = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Shorten Url')
        verbose_name_plural = _('Shorten Urls')

    @property
    def url(self):
        return self.get_redirect_url()

    def get_redirect_url(self, request=None):
        abs_url = getattr(settings, 'FQDN', None)
        if not abs_url and request:
            return request.build_absolute_uri()
        if not abs_url:
            logger.error(_('Cannot build redirect url, '
                           'please set FQDN in settings.py or '
                           'pass request object to get_redirect_rul()'))
            return self.shorten_url
        else:
            return '{}/{}'.format(abs_url.rstrip('/'), self.shorten_url)

    def set_shorten_url(self):
        if not self.shorten_url:
            self.shorten_url = short_url.encode_url(self.pk)
            self.save()
        return self.shorten_url
        
    def __str__(self):
        return '{} [{}]'.format(self.shorten_url, self.original_url)
