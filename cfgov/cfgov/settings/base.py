import os
from unipath import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))

# Application definition

INSTALLED_APPS = (
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'compressor',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'v1',
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
)

ROOT_URLCONF = 'cfgov.urls'

TEMPLATES = [
    {
        'NAME': 'wagtail-env',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'OPTIONS': {
            'environment': 'v1.environment'
        }
    },
    {
        'NAME': 'sheerlike-env',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'OPTIONS': {
            'environment': 'sheerlike.environment'
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    }
]

WSGI_APPLICATION = 'cfgov.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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
STATIC_ROOT = '/static/'

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Used to include directories not traditionally found app-specific 'static' directories
STATICFILES_DIRS = (
    # ...
    ("legacy", Path(os.path.dirname(__file__)).ancestor(2) + "/v1/static-legacy"),
)

ALLOWED_HOSTS = ['*']

# Wagtail settings

WAGTAIL_SITE_NAME = "v1"

# Sheer related settings

SHEER_SITES = [Path(os.path.dirname(__file__)).ancestor(2) + '/v1/jinja2/v1', Path(__file__).ancestor(4).child('docs')]
SHEER_ELASTICSEARCH_SERVER = os.environ.get('ES_HOST', 'localhost') + ':' + os.environ.get('ES_PORT', '9200')
SHEER_ELASTICSEARCH_INDEX = os.environ.get('SHEER_ELASTICSEARCH_INDEX', 'content')
