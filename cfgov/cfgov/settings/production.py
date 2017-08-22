import os
import sys

from .base import *
from os.path import exists

# log to disk when running in mod_wsgi, otherwise to console
if sys.argv and sys.argv[0] == 'mod_wsgi':
    default_loggers = ['syslog']
else:
    default_loggers = ['console', 'syslog']


# This allows the syslog stuff to work on OS X
syslog_device = next(l for l in ['/dev/log', '/var/run/syslog'] if exists(l))

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
        'syslog': {
            'address': syslog_device,
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'tagged'
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')

if not COLLECTSTATIC:
    if os.environ.get('DATABASE_ROUTING', False):

        DATABASES = {
            'default': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('MYSQL_NAME', ''),
                'USER': os.environ.get('MYSQL_USER', ''),
                'PASSWORD': os.environ.get('MYSQL_PW', ''),
                'HOST': os.environ.get('MYSQL_HOST', ''),
                'PORT': os.environ.get('MYSQL_PORT', ''),
            },
        }

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# allow us to configure the default MySQL storage engine, via the environment
if 'STORAGE_ENGINE' in os.environ:
    db_options = {'init_command': os.environ['STORAGE_ENGINE']}
    for db_label in DATABASES.keys():
        if 'mysql' in DATABASES[db_label]['ENGINE']:
            DATABASES[db_label]['OPTIONS'] = db_options
