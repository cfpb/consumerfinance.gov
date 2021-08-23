import json
import os
import sys
from os.path import exists

from django.core.exceptions import ImproperlyConfigured

from cfgov.settings.base import *


default_loggers = []

# Is there a syslog device available?
# selects first of these locations that exist, or None
syslog_device = next((l for l in ['/dev/log', '/var/run/syslog'] if exists(l)), None)

if syslog_device:
    default_loggers.append('syslog')

# if not running in mod_wsgi, add console logger
if not (sys.argv and sys.argv[0] == 'mod_wsgi'):
    default_loggers.append('console')

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
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': default_loggers,
            'level': 'INFO',
            'propagate': True,
        }
    }
}

if os.environ.get('SQS_QUEUE_ENABLED'):
    LOGGING['handlers']['sqs'] = {
        'level': 'ERROR',
        'class': 'alerts.logging_handlers.CFGovErrorHandler',
    }
    LOGGING['loggers']['django.request']['handlers'].append('sqs')

# Only add syslog to LOGGING if it's in default_loggers
if 'syslog' in default_loggers:
    LOGGING['handlers']['syslog'] = {
            'address': syslog_device,
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'tagged'
    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']

# ALLOWED_HOSTS should be defined as a JSON list in the ALLOWED_HOSTS
# environment variable.
try:
    ALLOWED_HOSTS = json.loads(os.getenv('ALLOWED_HOSTS'))
except (TypeError, ValueError):
    raise ImproperlyConfigured(
        "Environment variable ALLOWED_HOSTS is either not defined or is "
        "not valid JSON. Expected a JSON array of allowed hostnames."
    )
