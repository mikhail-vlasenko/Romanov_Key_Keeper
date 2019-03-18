"""
WSGI config for key_keeper project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""


# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u0678509/data/www/romanovkey.ru/key_keeper')
sys.path.insert(1, '/var/www/u0678509/data/djangoenv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'key_keeper.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
