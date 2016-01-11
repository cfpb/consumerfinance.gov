import os
from unipath import Path
from ..util import admin_emails

# Repository root is 4 levels above this file
REPOSITORY_ROOT = Path(__file__).ancestor(4)

# This is the root of the Django project, 'cfgov'
PROJECT_ROOT = REPOSITORY_ROOT.child('cfgov')
V1_TEMPLATE_ROOT = PROJECT_ROOT.child('jinja2', 'v1')

SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))
# Application definition

INSTALLED_APPS = (
    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtail.wagtailsites',

    'modelcluster',
    'compressor',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'localflavor',
    'flags',
    'v1',
    'core',
    'sheerlike',
)

MIDDLEWARE_CLASSES = (
    'sheerlike.middleware.GlobalRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',

    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

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
        'DIRS': [PROJECT_ROOT.child('static_built')],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'v1.environment',
            'extensions': [
                'wagtail.wagtailcore.jinja2tags.core',
                'wagtail.wagtailadmin.jinja2tags.userbar',
                'wagtail.wagtailimages.jinja2tags.images',
            ],
        }
    },
]

WSGI_APPLICATION = 'cfgov.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_NAME', 'v1'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PW', ''),
        'HOST': os.environ.get('MYSQL_HOST', ''),  # empty string == localhost
        'PORT': os.environ.get('MYSQL_PORT', ''),  # empty string == default
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', '/var/www/html/static')

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'f')
MEDIA_URL = '/f/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Used to include directories not traditionally found,
# app-specific 'static' directories.
STATICFILES_DIRS = [
    PROJECT_ROOT.child('static_built'),
    ('legacy', PROJECT_ROOT.child('v1', 'static-legacy')),
]

ALLOWED_HOSTS = ['*']

# Wagtail settings

WAGTAIL_SITE_NAME = 'v1'
WAGTAILIMAGES_IMAGE_MODEL = 'v1.CFGOVImage'

SHEER_SITES = [V1_TEMPLATE_ROOT]
SHEER_ELASTICSEARCH_SERVER = os.environ.get('ES_HOST', 'localhost') + ':' + os.environ.get('ES_PORT', '9200')
SHEER_ELASTICSEARCH_INDEX = os.environ.get('SHEER_ELASTICSEARCH_INDEX', 'content')

MAPPINGS = PROJECT_ROOT.child('es_mappings')
SHEER_PROCESSORS = \
    {
        "calendar_event": {
            "url": "$WORDPRESS/leadership-calendar/cfpb-leadership.json",
            "processor": "processors.django_calendar_event",
            "mappings": MAPPINGS.child("calendar_event.json")
        },
        "careers": {
            "url": "$WORDPRESS/jobs/jobs.json",
            "processor": "processors.django_career",
            "mappings": MAPPINGS.child("career.json")
        },
        "contact": {
            "url": "$WORDPRESS/api/get_posts/?post_type=contact",
            "processor": "processors.wordpress_contact",
            "mappings": MAPPINGS.child("contact.json")
        },
        "history": {
            "url": "$WORDPRESS/api/get_posts/?post_type=history",
            "processor": "processors.wordpress_history",
            "mappings": MAPPINGS.child("history.json")
        },
        "sub_page": {
            "url": "$WORDPRESS/api/get_posts/?post_type=sub_page",
            "processor": "processors.wordpress_sub_page",
            "mappings": MAPPINGS.child("sub_page.json")
        },
        "office": {
            "url": "$WORDPRESS/api/get_posts/?post_type=office",
            "processor": "processors.wordpress_office",
            "mappings": MAPPINGS.child("office.json")
        },
        "orgmember": {
            "url": "$WORDPRESS/api/get_posts/?post_type=orgmember",
            "processor": "processors.wordpress_orgmember",
            "mappings": MAPPINGS.child("orgmember.json")
        },
        "pages": {
            "url": "$WORDPRESS/api/get_posts/?post_type=page",
            "processor": "processors.wordpress_page",
            "mappings": MAPPINGS.child("pages.json")
        },
        "posts": {
            "url": "$WORDPRESS/api/get_posts/",
            "processor": "processors.wordpress_post",
            "mappings": MAPPINGS.child("posts.json")
        },
        "events": {
            "url": "$WORDPRESS/api/get_posts/?post_type=event",
            "processor": "processors.wordpress_event",
            "mappings": MAPPINGS.child("events.json")
        },
        "newsroom": {
            "url": "$WORDPRESS/api/get_posts/?post_type=cfpb_newsroom",
            "processor": "processors.wordpress_newsroom",
            "mappings": MAPPINGS.child("newsroom.json")
        },
        "views": {
            "url": "$WORDPRESS/api/get_posts/?post_type=view",
            "processor": "processors.wordpress_view",
            "mappings": MAPPINGS.child("views.json")
        },
        "featured_topic": {
            "url": "$WORDPRESS/api/get_posts/?post_type=featured_topic",
            "processor": "processors.wordpress_featured_topic",
            "mappings": MAPPINGS.child("featured_topic.json")
        },
        "faq": {
            "url": "$WORDPRESS/api/get_posts/?post_type=faq",
            "processor": "processors.wordpress_faq",
            "mappings": MAPPINGS.child("faq.json")
        }
    }

SHEER_ELASTICSEARCH_SETTINGS = \
    {
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_edge_ngram_analyzer": {
                        "tokenizer": "my_edge_ngram_tokenizer"
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

# S3 Configuration
if os.environ.get('S3_ENABLED', 'False') == 'True':
    DEFAULT_FILE_STORAGE = 'v1.s3utils.MediaRootS3BotoStorage'
    AWS_S3_SECURE_URLS = False  # True = use https; False = use http
    AWS_QUERYSTRING_AUTH = False  # False = do not use authentication-related query parameters for requests
    AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'

    MEDIA_URL = os.environ.get('AWS_S3_URL') + '/f/'

WAGTAIL_ENABLE_UPDATE_CHECK = False  # Removes wagtail version update check banner from admin page.

# Email
ADMINS = admin_emails(os.environ.get('ADMIN_EMAILS'))
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = os.environ.get('WAGTAILADMIN_NOTIFICATION_FROM_EMAIL')




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
LOGIN_FAIL_TIME_PERIOD = 120 * 60
# number of failed attempts
LOGIN_FAILS_ALLOWED = 5
