from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


DELTA_DAYS = getattr(settings, 'TINYURL_DURATION_DAYS', 7)


class UrlShortener(models.Model):
    # it could be also anonymous 
    user_id = models.ForeignKey(get_user_model(),
                                on_delete=models.SET_NULL,
                                blank=True, null=True)
    original_url = models.URLField()
    shorten_url = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Shorten Url')
        verbose_name_plural = _('Shorten Urls')

    def is_expired(self):
        # default 7 days
        if (timezone.now() - self.created).days >= DELTA_DAYS:
            return True 
        
    def __str__(self):
        return '{} [{}]'.format(self.shorten_url, self.original_url)
