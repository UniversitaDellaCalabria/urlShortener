import base64
import random
import string

from captcha.image import ImageCaptcha
from django.conf import settings

from . enc import encrypt


def get_captcha(text=None):
    fonts = getattr(settings, 'CAPTCHA_FONTS', None)
    length = getattr(settings, 'CAPTCHA_LENGTH', 5)
    image = ImageCaptcha(fonts=fonts)

    text = text or ''.join([random.choice(string.ascii_letters+string.hexdigits) for i in range(length)])
    data = image.generate(text)

    captcha_image_b64 = base64.b64encode(data.read()).decode()
    captcha_hidden_value = base64.b64encode(encrypt(text)).decode()
    return data, captcha_image_b64, captcha_hidden_value
