from .base import *

DEBUG = True
INSTALLED_APPS += ('django_extensions',)
STAGING_HOSTNAME = 'content.localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_NAME'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PW', ''),
        'HOST': '',  # Set to empty string for localhost
        'PORT': '',  # Set to empty string for default
    },
}
