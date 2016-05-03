from .base import *

DEBUG = True
INSTALLED_APPS += ('wagtail.contrib.wagtailstyleguide',)

DATABASES = {
    'default': {
        'ENGINE': MYSQL_ENGINE,
        'NAME': os.environ.get('MYSQL_NAME'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PW', ''),
        'HOST': os.environ.get('MYSQL_HOST', ''),  # empty string == localhost
        'PORT': os.environ.get('MYSQL_PORT', ''),  # empty string == default
        'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET storage_engine=MYISAM') },
    },
}

STATIC_ROOT = REPOSITORY_ROOT.child('collectstatic')

ALLOW_ADMIN_URL = DEBUG or os.environ.get('ALLOW_ADMIN_URL', False)
