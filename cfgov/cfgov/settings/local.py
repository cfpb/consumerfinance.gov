from .base import *

DEBUG = True
SECRET_KEY = 'not-secret-key-for-testing'
INSTALLED_APPS += (
    'sslserver',
    'wagtail.contrib.wagtailstyleguide',
)

if not COLLECTSTATIC:
    if os.environ.get('DATABASE_ROUTING', False):

        DATABASES = {
            'default': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('MYSQL_NAME', 'v1'),
                'USER': os.environ.get('MYSQL_USER', 'v1'),
                'PASSWORD': os.environ.get('MYSQL_PW', 'v1'),
                'HOST': os.environ.get('MYSQL_HOST', 'localhost.'),
                'PORT': os.environ.get('MYSQL_PORT', '3306'),
                'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET default_storage_engine=MYISAM') },
            },
            'legacy': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('LEGACY_MYSQL_NAME', 'legacy'),
                'USER': os.environ.get('LEGACY_MYSQL_USER', 'v1'),
                'PASSWORD': os.environ.get('LEGACY_MYSQL_PW', 'v1'),
                'HOST': os.environ.get('LEGACY_MYSQL_HOST', 'localhost.'),
                'PORT': os.environ.get('LEGACY_MYSQL_PORT', '3306'),
                'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET default_storage_engine=MYISAM') },
            },
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('MYSQL_NAME', 'v1'),
                'USER': os.environ.get('MYSQL_USER', 'v1'),
                'PASSWORD': os.environ.get('MYSQL_PW', 'v1'),
                'HOST': os.environ.get('MYSQL_HOST', 'localhost.'),
                'PORT': os.environ.get('MYSQL_PORT', '3306'),
                'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET default_storage_engine=MYISAM') },
                },
            }

STATIC_ROOT = REPOSITORY_ROOT.child('collectstatic')

ALLOW_ADMIN_URL = DEBUG or os.environ.get('ALLOW_ADMIN_URL', False)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# Django Debug Toolbar
if os.environ.get('ENABLE_DEBUG_TOOLBAR'):
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': True,
    }


MIDDLEWARE_CLASSES += CSP_MIDDLEWARE_CLASSES
CSP_REPORT_ONLY = True
