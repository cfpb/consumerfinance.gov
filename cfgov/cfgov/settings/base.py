
import os
import sys

from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

from unipath import Path

from ..util import admin_emails

# Repository root is 4 levels above this file
REPOSITORY_ROOT = Path(__file__).ancestor(4)

# This is the root of the Django project, 'cfgov'
PROJECT_ROOT = REPOSITORY_ROOT.child('cfgov')
V1_TEMPLATE_ROOT = PROJECT_ROOT.child('jinja2', 'v1')

SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))

# Deploy environment
DEPLOY_ENVIRONMENT = os.getenv('DEPLOY_ENVIRONMENT')

# signal that tells us that this is a proxied HTTPS request
# effects how request.is_secure() responds
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Use the django default password hashing
PASSWORD_HASHERS = global_settings.PASSWORD_HASHERS

# see https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-USE_ETAGS
USE_ETAGS = True

# Application definition

INSTALLED_APPS = (
    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.contrib.wagtailfrontendcache',
#    'wagtail.wagtailsearch', # TODO: conflicts with haystack, will need to revisit.
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtail.wagtailsites',

    'wagtail.contrib.modeladmin',
    'wagtail.contrib.table_block',
    'wagtail.contrib.wagtailroutablepage',
    'localflavor',
    'modelcluster',
    'compressor',
    'taggit',
    'wagtailsharing',
    'flags',
    'watchman',
    'haystack',
    'ask_cfpb',
    'overextends',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'storages',
    'data_research',
    'v1',
    'core',
    'sheerlike',
    'legacy',
    'django_extensions',
    'reversion',
    'tinymce',
    'jobmanager',
    'wellbeing',
)

OPTIONAL_APPS = [
    {'import': 'comparisontool', 'apps': ('comparisontool', 'haystack',)},
    {'import': 'paying_for_college',
     'apps': ('paying_for_college', 'haystack',)},
    {'import': 'agreements', 'apps': ('agreements', 'haystack',)},
    {'import': 'selfregistration', 'apps': ('selfregistration',)},
    {'import': 'hud_api_replace', 'apps': ('hud_api_replace',)},
    {'import': 'retirement_api', 'apps': ('retirement_api',)},
    {'import': 'complaint', 'apps': ('complaint',
     'complaintdatabase', 'complaint_common',)},
    {'import': 'ratechecker', 'apps': ('ratechecker', 'rest_framework')},
    {'import': 'countylimits', 'apps': ('countylimits', 'rest_framework')},
    {'import': 'regcore', 'apps': ('regcore', 'regcore_read', 'regcore_write')},
    {'import': 'eregsip', 'apps': ('eregsip',)},
    {'import': 'regulations', 'apps': ('regulations',)},
    {'import': 'complaint_search', 'apps': ('complaint_search', 'rest_framework')},
    {'import': 'ccdb5_ui', 'apps': ('ccdb5_ui', )},
]

if DEPLOY_ENVIRONMENT == 'build':
    OPTIONAL_APPS += [
        {'import': 'eregs_core', 'apps': ('eregs_core',)},
    ]

MIDDLEWARE_CLASSES = (
    'sheerlike.middleware.GlobalRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    'v1.middleware.StagingMiddleware',
    'core.middleware.DownstreamCacheControlMiddleware'
)

CSP_MIDDLEWARE_CLASSES = ('csp.middleware.CSPMiddleware', )

if ('CSP_ENFORCE' in os.environ or 'CSP_REPORT' in os.environ):
    MIDDLEWARE_CLASSES += CSP_MIDDLEWARE_CLASSES

if 'CSP_REPORT' in os.environ:
    CSP_REPORT_ONLY = True

CSP_REPORT_URI = '/csp-report/'

ROOT_URLCONF = 'cfgov.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_ROOT.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
    {
        'NAME': 'wagtail-env',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            V1_TEMPLATE_ROOT,
            V1_TEMPLATE_ROOT.child('_includes'),
            V1_TEMPLATE_ROOT.child('_layouts'),
            PROJECT_ROOT.child('static_built'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'v1.environment',
            'extensions': [
                'v1.jinja2tags.images',
                'wagtail.wagtailcore.jinja2tags.core',
                'wagtail.wagtailadmin.jinja2tags.userbar',
                'wagtail.wagtailimages.jinja2tags.images',
            ],
        }
    },
]

WSGI_APPLICATION = 'cfgov.wsgi.application'

# Admin Url Access
ALLOW_ADMIN_URL = os.environ.get('ALLOW_ADMIN_URL', False)

DATABASE_ROUTERS = ['v1.db_router.CFGOVRouter']


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', '/var/www/html/static')

MEDIA_ROOT = os.environ.get('MEDIA_ROOT',
                            os.path.join(PROJECT_ROOT, 'f'))
MEDIA_URL = '/f/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'sheerlike.finders.SheerlikeStaticFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Used to include directories not traditionally found,
# app-specific 'static' directories.
STATICFILES_DIRS = [
    PROJECT_ROOT.child('static_built'),
    PROJECT_ROOT.child('templates', 'wagtailadmin')
]


ALLOWED_HOSTS = ['*']

EXTERNAL_URL_WHITELIST = (r'^https:\/\/facebook\.com\/cfpb$',
                          r'^https:\/\/twitter\.com\/cfpb$',
                          r'^https:\/\/www\.linkedin\.com\/company\/consumer-financial-protection-bureau$',
                          r'^https:\/\/www\.youtube\.com\/user\/cfpbvideo$',
                          r'https:\/\/www\.flickr\.com\/photos\/cfpbphotos$'
                          )
EXTERNAL_LINK_PATTERN = r'https?:\/\/(?:www\.)?(?![^\?]+gov)(?!(content\.)?localhost).*'
NONCFPB_LINK_PATTERN = r'(https?:\/\/(?:www\.)?(?![^\?]*(cfpb|consumerfinance).gov)(?!(content\.)?localhost).*)'
FILES_LINK_PATTERN = r'https?:\/\/files\.consumerfinance.gov\/f\/\S+\.[a-z]+'
DOWNLOAD_LINK_PATTERN = r'(\.pdf|\.doc|\.docx|\.xls|\.xlsx|\.csv|\.zip)$'

# Wagtail settings

WAGTAIL_SITE_NAME = 'consumerfinance.gov'
WAGTAILIMAGES_IMAGE_MODEL = 'v1.CFGOVImage'
TAGGIT_CASE_INSENSITIVE = True

WAGTAIL_USER_CREATION_FORM = 'v1.auth_forms.UserCreationForm'
WAGTAIL_USER_EDIT_FORM = 'v1.auth_forms.UserEditForm'

SHEER_ELASTICSEARCH_SERVER = os.environ.get('ES_HOST', 'localhost') + ':' + os.environ.get('ES_PORT', '9200')
SHEER_ELASTICSEARCH_INDEX = os.environ.get('SHEER_ELASTICSEARCH_INDEX', 'content')
ELASTICSEARCH_BIGINT = 50000

MAPPINGS = PROJECT_ROOT.child('es_mappings')

SHEER_ELASTICSEARCH_SETTINGS = \
    {
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_edge_ngram_analyzer": {
                        "tokenizer": "my_edge_ngram_tokenizer"
                    },
                    "tag_analyzer": {
                       "tokenizer": "keyword",
                       "filter": "lowercase"
                    }
                },
                "tokenizer": {
                    "my_edge_ngram_tokenizer": {
                        "type": "edgeNGram",
                        "min_gram": "2",
                        "max_gram": "5",
                        "token_chars": [
                            "letter",
                            "digit"
                        ]
                    }
                }
            }
        }
    }


# PDFReactor
PDFREACTOR_LIB = os.environ.get('PDFREACTOR_LIB', '/opt/PDFreactor/wrappers/python/lib')

#LEGACY APPS

STATIC_VERSION = ''

# DJANGO HUD API
DJANGO_HUD_API_ENDPOINT= os.environ.get('HUD_API_ENDPOINT', 'http://localhost/hud-api-replace/')
# in seconds, 2592000 == 30 days. Google allows no more than a month of caching
DJANGO_HUD_GEODATA_EXPIRATION_INTERVAL = 2592000
MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN')
HOUSING_COUNSELOR_S3_PATH_TEMPLATE = (
    'a/assets/hud/{format}s/{zipcode}.{format}'
)


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': SHEER_ELASTICSEARCH_SERVER,
        'INDEX_NAME': os.environ.get('HAYSTACK_ELASTICSEARCH_INDEX', SHEER_ELASTICSEARCH_INDEX+'_haystack'),
    },
}

# S3 Configuration
AWS_QUERYSTRING_AUTH = False  # do not add auth-related query params to URL
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
AWS_S3_ROOT = os.environ.get('AWS_S3_ROOT', 'f')
AWS_S3_SECURE_URLS = True  # True = use https; False = use http
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

if os.environ.get('S3_ENABLED', 'False') == 'True':
    DEFAULT_FILE_STORAGE = 'v1.s3utils.MediaRootS3BotoStorage'
    AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')
    MEDIA_URL = os.path.join(os.environ.get('AWS_S3_URL'), AWS_S3_ROOT, '')

# Govdelivery

GOVDELIVERY_USER = os.environ.get('GOVDELIVERY_USER')
GOVDELIVERY_PASSWORD = os.environ.get('GOVDELIVERY_PASSWORD')
GOVDELIVERY_ACCOUNT_CODE = os.environ.get('GOVDELIVERY_ACCOUNT_CODE')

# LOAD OPTIONAL APPS
# code from https://gist.github.com/msabramo/945406

for app in OPTIONAL_APPS:
    try:
        __import__(app["import"])
        for name in app.get("apps", ()):
            if name not in INSTALLED_APPS:
                INSTALLED_APPS += (name,)
        MIDDLEWARE_CLASSES += app.get("middleware", ())
    except ImportError:
        pass

WAGTAIL_ENABLE_UPDATE_CHECK = False  # Removes wagtail version update check banner from admin page.

# Email
ADMINS = admin_emails(os.environ.get('ADMIN_EMAILS'))

if DEPLOY_ENVIRONMENT:
    EMAIL_SUBJECT_PREFIX = u'[{}] '.format(DEPLOY_ENVIRONMENT.title())

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = os.environ.get(
    'WAGTAILADMIN_NOTIFICATION_FROM_EMAIL')


# Password Policies
# cfpb_common password rules
CFPB_COMMON_PASSWORD_RULES = [
    [r'.{12,}', 'Minimum allowed length is 12 characters'],
    [r'[A-Z]', 'Password must include at least one capital letter'],
    [r'[a-z]', 'Password must include at least one lowercase letter'],
    [r'[0-9]', 'Password must include at least one digit'],
    [r'[@#$%&!]', 'Password must include at least one special character (@#$%&!)'],
]
# cfpb_common login rules
# in seconds
LOGIN_FAIL_TIME_PERIOD = os.environ.get('LOGIN_FAIL_TIME_PERIOD', 120 * 60)
# number of failed attempts
LOGIN_FAILS_ALLOWED = os.environ.get('LOGIN_FAILS_ALLOWED', 5)
LOGIN_REDIRECT_URL = '/login/welcome/'
LOGIN_URL = "/login/"


SHEER_SITES = {
    'assets': V1_TEMPLATE_ROOT,
    'owning-a-home':
        Path(os.environ.get('OAH_SHEER_PATH') or
             Path(REPOSITORY_ROOT, '../owning-a-home/dist')),
    'fin-ed-resources':
        Path(os.environ.get('FIN_ED_SHEER_PATH') or
             Path(REPOSITORY_ROOT, '../fin-ed-resources/dist')),
    'know-before-you-owe':
        Path(os.environ.get('KBYO_SHEER_PATH') or
             Path(REPOSITORY_ROOT, '../know-before-you-owe/dist')),
}

# The base URL for the API that we use to access layers and the regulation.
API_BASE = os.environ.get('EREGS_API_BASE', '')

# When we generate an full HTML version of the regulation, we want to
# write it out somewhere. This is where.
OFFLINE_OUTPUT_DIR = ''

DATE_FORMAT = 'n/j/Y'

GOOGLE_ANALYTICS_ID = ''
GOOGLE_ANALYTICS_SITE = ''

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_KEY_PREFIX = 'eregs'
CACHE_MIDDLEWARE_SECONDS = 1800

# eRegs
BACKENDS = {
    'regulations': 'regcore.db.django_models.DMRegulations',
    'layers': 'regcore.db.django_models.DMLayers',
    'notices': 'regcore.db.django_models.DMNotices',
    'diffs': 'regcore.db.django_models.DMDiffs',
}

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


# GovDelivery environment variables
ACCOUNT_CODE = os.environ.get('GOVDELIVERY_ACCOUNT_CODE')

# Regulations.gov environment variables
REGSGOV_BASE_URL = os.environ.get('REGSGOV_BASE_URL')
REGSGOV_API_KEY = os.environ.get('REGSGOV_API_KEY')

# Akamai
ENABLE_AKAMAI_CACHE_PURGE = os.environ.get('ENABLE_AKAMAI_CACHE_PURGE', False)
if ENABLE_AKAMAI_CACHE_PURGE:
    WAGTAILFRONTENDCACHE = {
        'akamai': {
            'BACKEND': 'v1.models.akamai_backend.AkamaiBackend',
            'CLIENT_TOKEN': os.environ.get('AKAMAI_CLIENT_TOKEN'),
            'CLIENT_SECRET': os.environ.get('AKAMAI_CLIENT_SECRET'),
            'ACCESS_TOKEN': os.environ.get('AKAMAI_ACCESS_TOKEN')
        },
    }


# Staging site
STAGING_HOSTNAME = os.environ.get('DJANGO_STAGING_HOSTNAME')

# CSP Whitelists

# These specify what is allowed in <script> tags.
CSP_SCRIPT_SRC = ("'self'",
                  "'unsafe-inline'",
                  "'unsafe-eval'",
                  '*.google-analytics.com',
                  '*.googletagmanager.com',
                  'ajax.googleapis.com',
                  'search.usa.gov',
                  'api.mapbox.com',
                  'js-agent.newrelic.com',
                  'dnn506yrbagrg.cloudfront.net',
                  '*.doubleclick.net',
                  'bam.nr-data.net',
                  '*.youtube.com',
                  '*.ytimg.com',
                  'trk.cetrk.com',
                  'universal.iperceptions.com',
                  'sample.crazyegg.com',
                  'about:'
                  )

# These specify valid sources of CSS code
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'fast.fonts.net',
    'api.mapbox.com')

# These specify valid image sources
CSP_IMG_SRC = (
    "'self'",
    's3.amazonaws.com',
    'stats.g.doubleclick.net',
    'files.consumerfinance.gov',
    'img.youtube.com',
    '*.google-analytics.com',
    'trk.cetrk.com',
    'searchstats.usa.gov',
    'gtrk.s3.amazonaws.com',
    '*.googletagmanager.com',
    'api.mapbox.com',
    '*.tiles.mapbox.com',
    'stats.search.usa.gov',
    'data:')

# These specify what URL's we allow to appear in frames/iframes
CSP_FRAME_SRC = (
    "'self'",
    '*.googletagmanager.com',
    '*.google-analytics.com',
    'www.youtube.com',
    '*.doubleclick.net',
    'universal.iperceptions.com')

# These specify where we allow fonts to come from
CSP_FONT_SRC = ("'self'", 'fast.fonts.net')

# These specify hosts we can make (potentially) cross-domain AJAX requests to.
CSP_CONNECT_SRC = ("'self'",
                   '*.tiles.mapbox.com',
                   'bam.nr-data.net',
                   'files.consumerfinance.gov',
                   's3.amazonaws.com',
                   'api.iperceptions.com')

# Feature flags
# All feature flags must be listed here with a dict of any hard-coded
# conditions or an empty dict. If the conditions dict is empty the flag will
# only be enabled if database conditions are added.
FLAGS = {
    # Beta banner, seen on beta.consumerfinance.gov
    # When enabled, a banner appears across the top of the site proclaiming
    # "This beta site is a work in progress."
    'BETA_NOTICE': {
        'site': 'beta.consumerfinance.gov',
    },

    # When enabled, Display a "techical issues" banner on /complaintdatabase
    'CCDB_TECHNICAL_ISSUES': {},

    # IA changes to mega menu for user testing
    # When enabled, the mega menu under "Consumer Tools" is arranged by topic
    'IA_USER_TESTING_MENU': {},

    # Fix for margin-top when using the text inset
    # When enabled, the top margin of full-width text insets is increased
    'INSET_TEST': {},

    # When enabled, serves `/es/` pages from this
    # repo ( excluding /obtener-respuestas/ pages ).
    'ES_CONV_FLAG': {},

    # Transition of "About Us" to Wagtail
    # When enabled, the "About Us" pages are served from Wagtail
    'WAGTAIL_ABOUT_US': {},

    # Transition of "Doing Business with Us" to Wagtail
    # When enabled, the "Doing Business With Us" pages are served from Wagtail
    'WAGTAIL_DOING_BUSINESS_WITH_US': {},

    # The next version of the public consumer complaint database
    'CCDB5_RELEASE': {},

    # Google Optimize code snippets for A/B testing
    # When enabled this flag will add various Google Optimize code snippets.
    # Intended for use with path conditions.
    'AB_TESTING': {},


    # The next version of eRegulations
    'EREGS20': {
        'boolean': DEPLOY_ENVIRONMENT == 'build',
    },

    # Add sortable tables to Wagtail
    # When enabled, the sortable tables option will be added to the Wagtail Admin
    # The template will render for the front-end, but the sortable code is missing
    # and the table will not be sortable until cf-tables from CF 4.x is implemented
    'SORTABLE_TABLES': {},

    # The release of the consumer Financial Well Being Scale app
    'FWB_RELEASE': {},
}


# Watchman tokens, used to authenticate global status endpoint
WATCHMAN_TOKENS = os.environ.get('WATCHMAN_TOKENS', os.urandom(32))

# This specifies what checks Watchman should run and include in its output
# https://github.com/mwarkentin/django-watchman#custom-checks
WATCHMAN_CHECKS = (
    'watchman.checks.databases',
    'watchman.checks.storage',
    'watchman.checks.caches',
    'alerts.checks.check_clock_drift',
)

# Used to check server's time against in check_clock_drift
NTP_TIME_SERVER = 'north-america.pool.ntp.org'

# If server's clock drifts from NTP by more than specified offset
# (in seconds), check_clock_drift will fail
MAX_ALLOWED_TIME_OFFSET = 5
