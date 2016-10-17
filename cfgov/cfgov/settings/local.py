from .base import *

DEBUG = True
INSTALLED_APPS += (
    'sslserver',
    'wagtail.contrib.wagtailstyleguide',
)

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
            'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET storage_engine=MYISAM') },
        },
        'legacy': {
            'ENGINE': MYSQL_ENGINE,
            'NAME': os.environ.get('LEGACY_MYSQL_NAME', ''),
            'USER': os.environ.get('LEGACY_MYSQL_USER', ''),
            'PASSWORD': os.environ.get('LEGACY_MYSQL_PW', ''),
            'HOST': os.environ.get('LEGACY_MYSQL_HOST', ''),
            'PORT': os.environ.get('LEGACY_MYSQL_PORT', ''),
            'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET storage_engine=MYISAM') },
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': MYSQL_ENGINE,
            'NAME': os.environ.get('MYSQL_NAME', ''),
            'USER': os.environ.get('MYSQL_USER', ''),
            'PASSWORD': os.environ.get('MYSQL_PW', ''),
            'HOST': os.environ.get('MYSQL_HOST', ''),
            'PORT': os.environ.get('MYSQL_PORT', ''),
            'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET storage_engine=MYISAM') },
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

# CSP

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('csp.middleware.CSPMiddleware',)
CSP_REPORT_ONLY = True

CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'","'unsafe-eval'", '*.google-analytics.com',
                  '*.googletagmanager.com', 'search.usa.gov', 'api.mapbox.com',
                  'js-agent.newrelic.com', 'dnn506yrbagrg.cloudfront.net',
                  '*.doubleclick.net', 'bam.nr-data.net',  '*.youtube.com',
                  '*.ytimg.com', 'trk.cetrk.com')

CSP_STYLE_SRC= ("'self'", "'unsafe-inline'", 'fast.fonts.net', 'api.mapbox.com')
CSP_IMG_SRC= ("'self'",'s3.amazonaws.com', 'stats.g.doubleclick.net',
              'files.consumerfinance.gov', 'img.youtube.com',
              '*.google-analytics.com', 'trk.cetrk.com', 'searchstats.usa.gov',
              'gtrk.s3.amazonaws.com')
CSP_FRAME_SRC= ("'self'", '*.googletagmanager.com', '*.google-analytics.com',
                'www.youtube.com', '*.doubleclick.net')
CSP_FONT_SRC = ("'self'", 'fast.fonts.net')
