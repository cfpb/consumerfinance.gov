from .base import *

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
        'disk': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv('CFGOV_DJANGO_LOG'),
            'maxBytes': 1024*1024*10,  # max 10 MB per file
            'backupCount': 5,  # keep 5 files around
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
            'handlers': ['disk'],
            'level': 'INFO',
            'propagate': True,
        }
    }
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
