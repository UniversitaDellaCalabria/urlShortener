from django import forms
from django.utils.translation import gettext as _

from . enc import decrypt


class UrlShortenerForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    captcha = forms.CharField()
    captcha_hidden = forms.CharField(widget=forms.HiddenInput())

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha', '')
        hcaptcha = cleaned_data.get('captcha_hidden', '')
        try:
            dcaptcha = decrypt(hcaptcha).decode()
        except:
            dcaptcha = ''
        if '' in (captcha, dcaptcha) or \
            dcaptcha.lower() != captcha.lower():
            errors = self.add_error('captcha',
                                    _('You have inserted an invalid captcha value !'))
