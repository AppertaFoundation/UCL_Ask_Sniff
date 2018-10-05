"""
WSGI config for asksniff project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asksniff.settings")

if config('PRODUCTION', cast=bool):
    os.environ['HTTPS'] = "on"
    
application = DjangoWhiteNoise(get_wsgi_application())

