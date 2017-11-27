import os
import sys

from os.path import exists

from .base import *
from .mysql_mixin import *


# log to disk when running in mod_wsgi, otherwise to console
if sys.argv and sys.argv[0] == 'mod_wsgi':
    default_loggers = ['syslog']
    # Every so often, these files temporarily do not exist on the server
    # If so, set device to None and don't add syslog in LOGGING
    syslog_device = next((l for l in ['/dev/log', '/var/run/syslog'] if exists(l)), default=None)
else:
    default_loggers = ['console', 'syslog']

# Sends an email to developers in the ADMIN_EMAILS list if Debug=False for errors
#
# in the formatter, "django: " is an rsyslog tag. This is equivalent to:
#     logger -t django "my log message"
# on the server, the tag will be used to route the message to the desired
# logfile
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'tagged': {
            'format': 'django: %(message)s'
                  },
    },
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
        'db': {
            'level': 'ERROR',
            'class': 'alerts.logging_handlers.CFGovErrorHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'db'],
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
        },
        'core.views': {
            'handlers': default_loggers,
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# Only add syslog to LOGGING if not syslog_device exists
if syslog_device is not None:
    LOGGING['handlers']['syslog'] = {
            'address': syslog_device,
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'tagged'
    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Define caches necessary for eRegs.
CACHES = {
    'default' : {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/eregs_cache',
    },
    'eregs_longterm_cache': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/eregs_longterm_cache',
        'TIMEOUT': 60*60*24*15,     # 15 days
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
        },
    },
    'api_cache':{
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'api_cache_memory',
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        },
    }
}
