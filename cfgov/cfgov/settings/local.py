import warnings

from unipath import DIRS

from .base import *


DEBUG = True
SECRET_KEY = 'not-secret-key-for-testing'
INSTALLED_APPS += (
    'sslserver',
    'wagtail.contrib.wagtailstyleguide',
)

STATIC_ROOT = REPOSITORY_ROOT.child('collectstatic')
STATICFILES_DIRS += [str(d) for d in REPOSITORY_ROOT.child('static.in').listdir(filter=DIRS)]

ALLOW_ADMIN_URL = DEBUG or os.environ.get('ALLOW_ADMIN_URL', False)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
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

# Log database queries.
if os.environ.get('ENABLE_SQL_LOGGING'):
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    }

# Django Debug Toolbar
if os.environ.get('ENABLE_DEBUG_TOOLBAR'):
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = (os.environ.get('INTERNAL_IP', '127.0.0.1'), )

    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': True,
    }


MIDDLEWARE_CLASSES += CSP_MIDDLEWARE_CLASSES

# Disable caching when working locally.
CACHES.update({
    k: {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'TIMEOUT': 0,
    } for k in (
        'default', 'post_preview'
    )
})

# Optionally enable cache for post_preview
if os.environ.get('ENABLE_POST_PREVIEW_CACHE'):
    CACHES['post_preview'] = {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'post_preview_cache',
        'TIMEOUT': None,
    }

# Use a mock GovDelivery API instead of the real thing,
# unless the GOVDELIVERY_BASE_URL environment variable is set.
if not os.environ.get('GOVDELIVERY_BASE_URL'):
    GOVDELIVERY_API = 'core.govdelivery.LoggingMockGovDelivery'
