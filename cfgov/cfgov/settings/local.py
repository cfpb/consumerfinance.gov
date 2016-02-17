from .base import *

DEBUG = True
INSTALLED_APPS += ('django_extensions', 'wagtail.contrib.wagtailstyleguide')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_NAME', 'cfgov'),
        'USER': os.environ.get('MYSQL_USER', 'cfgov'),
        'PASSWORD': os.environ.get('MYSQL_PW', 'cfgov123'),
        'HOST': os.environ.get('MYSQL_HOST', ''),  # empty string == localhost
        'PORT': os.environ.get('MYSQL_PORT', ''),  # empty string == default
    },
}

STATIC_ROOT = REPOSITORY_ROOT.child('collectstatic')
