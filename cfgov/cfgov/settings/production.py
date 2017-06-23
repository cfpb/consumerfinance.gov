import sys

from .base import *

# log to disk when running in mod_wsgi, otherwise to console
# This avoids permissions problems when logged in users (or CI jobs)
# can't write to the log file.
if sys.argv and sys.argv[0] == 'mod_wsgi':
    default_loggers = ['disk']
else:
    default_loggers = ['console']

# Sends an email to developers in the ADMIN_EMAILS list if Debug=False for errors
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'level': 'ERROR',
            'propagate': False,
        },
        'v1': {
            'handlers': default_loggers,
            'level': 'INFO',
            'propagate': True,
        }
    }
}

if 'disk' in default_loggers:
   LOGGING['handlers']['disk'] = {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv('CFGOV_DJANGO_LOG'),
            'maxBytes': 1024*1024*10,  # max 10 MB per file
            'backupCount': 5,  # keep 5 files around
        }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')

if not COLLECTSTATIC:
    if os.environ.get('DATABASE_ROUTING', False):
        DATABASE_ROUTERS = ['v1.db_router.CFGOVRouter', 'v1.db_router.LegacyRouter']

        DATABASES = {
            'default': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('MYSQL_NAME', ''),
                'USER': os.environ.get('MYSQL_USER', ''),
                'PASSWORD': os.environ.get('MYSQL_PW', ''),
                'HOST': os.environ.get('MYSQL_HOST', ''),
                'PORT': os.environ.get('MYSQL_PORT', ''),
            },
            'legacy': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('LEGACY_MYSQL_NAME', ''),
                'USER': os.environ.get('LEGACY_MYSQL_USER', ''),
                'PASSWORD': os.environ.get('LEGACY_MYSQL_PW', ''),
                'HOST': os.environ.get('LEGACY_MYSQL_HOST', ''),
                'PORT': os.environ.get('LEGACY_MYSQL_PORT', ''),
            },
        }

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
