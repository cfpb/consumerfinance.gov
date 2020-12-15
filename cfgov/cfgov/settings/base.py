import os
from pathlib import Path

from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

import dj_database_url
from elasticsearch7 import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from cfgov.util import admin_emails


# Repository root is 4 levels above this file
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

# This is the root of the Django project, 'cfgov'
PROJECT_ROOT = REPOSITORY_ROOT.joinpath("cfgov")
V1_TEMPLATE_ROOT = PROJECT_ROOT.joinpath("jinja2", "v1")

SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))

# Deploy environment
DEPLOY_ENVIRONMENT = os.getenv("DEPLOY_ENVIRONMENT")

# In certain environments, we allow DEBUG to be enabled
DEBUG = os.environ.get("DJANGO_DEBUG") == "True"

# signal that tells us that this is a proxied HTTPS request
# effects how request.is_secure() responds
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# in some environments, we want to respect X-Forwarded-Port
USE_X_FORWARDED_PORT = os.environ.get("USE_X_FORWARDED_PORT") == "True"

# Use the django default password hashing
PASSWORD_HASHERS = global_settings.PASSWORD_HASHERS

# Application definition
INSTALLED_APPS = (
    "permissions_viewer",
    "wagtail.core",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.users",
    "wagtail.images",
    "wagtail.embeds",
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.redirects",
    "wagtail.contrib.forms",
    "wagtail.sites",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.table_block",
    "wagtail.contrib.postgres_search",
    "localflavor",
    "modelcluster",
    "taggit",
    "wagtailinventory",
    "wagtailsharing",
    "flags",
    "wagtailautocomplete",
    "wagtailflags",
    "watchman",
    "haystack",
    "ask_cfpb",
    "agreements",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "wagtail.search",
    "storages",
    "data_research",
    "v1",
    "core",
    "legacy",
    "django_extensions",
    "jobmanager",
    "wellbeing",
    "search",
    "paying_for_college",
    "prepaid_agreements",
    "regulations3k",
    "treemodeladmin",
    "housing_counselor",
    "hmda",
    "youth_employment",
    "diversity_inclusion",
    "mega_menu.apps.MegaMenuConfig",
    "form_explainer.apps.FormExplainerConfig",
    "teachers_digital_platform",
    "wagtailmedia",
    "django_elasticsearch_dsl",

    # Satellites
    "comparisontool",
    "retirement_api",
    "ratechecker",
    "countylimits",
    "complaint_search",
    "rest_framework",
    "ccdb5_ui",
    "mptt",
    "crtool",
)

WAGTAILSEARCH_BACKENDS = {
    # The default search backend for Wagtail is the db backend, which does not
    # support the custom search_fields defined on Page model descendents when
    # using `Page.objects.search()`.
    #
    # Other backends *do* support those custom search_fields, so for now to
    # preserve the current behavior of /admin/pages/search (which calls
    # `Page.objects.search()`), the default backend will remain `db`.
    #
    # This also preserves the current behavior of our external link search,
    # /admin/external-links/, which calls each page model's `objects.search()`
    # explicitly to get results, but which returns fewer results with the
    # Postgres full text backend.
    #
    # An upcoming effort to overhaul search within consumerfinance.gov and
    # Wagtail should address these issues. In the meantime, Postgres full text
    # search with the custom search_fields defined on our models is available
    # with the "fulltext" backend defined below.
    'default': {
        'BACKEND': 'wagtail.search.backends.db',
    },
    'fulltext': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
    },
}

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "core.middleware.ParseLinksMiddleware",
    "core.middleware.DownstreamCacheControlMiddleware",
    "flags.middleware.FlagConditionsMiddleware",
    "core.middleware.SelfHealingMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "core.middleware.DeactivateTranslationsMiddleware",
)

CSP_MIDDLEWARE = ("csp.middleware.CSPMiddleware",)

if "CSP_ENFORCE" in os.environ:
    MIDDLEWARE += CSP_MIDDLEWARE

ROOT_URLCONF = "cfgov.urls"

# We support two different template engines: Django templates and Jinja2
# templates. See https://docs.djangoproject.com/en/dev/topics/templates/
# for an overview of how Django templates work.

wagtail_extensions = [
    "wagtail.core.jinja2tags.core",
    "wagtail.admin.jinja2tags.userbar",
    "wagtail.images.jinja2tags.images",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Look for Django templates in these directories
        "DIRS": [PROJECT_ROOT.joinpath("templates")],
        # Look for Django templates in each app under a templates subdirectory
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "NAME": "wagtail-env",
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        # Look for Jinja2 templates in these directories
        "DIRS": [
            V1_TEMPLATE_ROOT,
            V1_TEMPLATE_ROOT.joinpath("_includes"),
            V1_TEMPLATE_ROOT.joinpath("_layouts"),
            PROJECT_ROOT.joinpath("static_built"),
        ],
        # Look for Jinja2 templates in each app under a jinja2 subdirectory
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "v1.jinja2_environment.environment",
            "extensions": wagtail_extensions
            + [
                "jinja2.ext.do",
                "jinja2.ext.i18n",
                "jinja2.ext.loopcontrols",
                "flags.jinja2tags.flags",
                "core.jinja2tags.filters",
                "agreements.jinja2tags.agreements",
                "mega_menu.jinja2tags.MegaMenuExtension",
                "prepaid_agreements.jinja2tags.prepaid_agreements",
                "regulations3k.jinja2tags.regulations",
                "v1.jinja2tags.datetimes_extension",
                "v1.jinja2tags.fragment_cache_extension",
                "v1.jinja2tags.v1_extension",
            ],
        },
    },
]

WSGI_APPLICATION = "cfgov.wsgi.application"

# Admin Url Access
ALLOW_ADMIN_URL = os.environ.get("ALLOW_ADMIN_URL", False)

if ALLOW_ADMIN_URL:
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000  # For heavy Wagtail pages

# Databases
DATABASES = {}

# If DATABASE_URL is defined in the environment, use it to set the Django DB
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
)

LOCALE_PATHS = (os.path.join(PROJECT_ROOT, "locale"),)

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/
STATIC_URL = "/static/"

MEDIA_ROOT = os.environ.get("MEDIA_ROOT", os.path.join(PROJECT_ROOT, "f"))
MEDIA_URL = "/f/"


# List of finder classes that know how to find static files in
# various locations
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Used to include directories not traditionally found,
# app-specific 'static' directories.
STATICFILES_DIRS = [
    PROJECT_ROOT.joinpath("static_built"),
    PROJECT_ROOT.joinpath("templates", "wagtailadmin"),
]

# Also include any directories under static.in
STATICFILES_DIRS += [
    d for d in REPOSITORY_ROOT.joinpath("static.in").iterdir() if d.is_dir()
]

ALLOWED_HOSTS = ["*"]

EXTERNAL_URL_ALLOWLIST = (
    r"^https:\/\/facebook\.com\/cfpb$",
    r"^https:\/\/twitter\.com\/cfpb$",
    r"^https:\/\/www\.linkedin\.com\/company\/consumer-financial-protection-bureau$",  # noqa 501
    r"^https:\/\/www\.youtube\.com\/user\/cfpbvideo$",
    r"https:\/\/www\.flickr\.com\/photos\/cfpbphotos$",
)

# Wagtail settings
WAGTAIL_SITE_NAME = "consumerfinance.gov"
WAGTAILIMAGES_IMAGE_MODEL = "v1.CFGOVImage"
TAGGIT_CASE_INSENSITIVE = True

WAGTAIL_USER_CREATION_FORM = "v1.auth_forms.UserCreationForm"
WAGTAIL_USER_EDIT_FORM = "v1.auth_forms.UserEditForm"

SHEER_ELASTICSEARCH_SERVER = (
    os.environ.get("ES_HOST", "localhost")
    + ":"
    + os.environ.get("ES_PORT", "9200")
)
SHEER_ELASTICSEARCH_INDEX = os.environ.get(
    "SHEER_ELASTICSEARCH_INDEX", "content"
)
ELASTICSEARCH_BIGINT = 50000

SHEER_ELASTICSEARCH_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_edge_ngram_analyzer": {
                    "tokenizer": "my_edge_ngram_tokenizer"
                },
                "tag_analyzer": {
                    "tokenizer": "keyword",
                    "filter": "lowercase",
                },
            },
            "tokenizer": {
                "my_edge_ngram_tokenizer": {
                    "type": "edgeNGram",
                    "min_gram": "2",
                    "max_gram": "5",
                    "token_chars": ["letter", "digit"],
                }
            },
        }
    }
}


# LEGACY APPS
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")

HOUSING_COUNSELOR_S3_PATH_TEMPLATE = (
    "https://s3.amazonaws.com/files.consumerfinance.gov"
    "/a/assets/hud/{file_format}s/{zipcode}.{file_format}"
)

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "search.backends.CFGOVElasticsearch2SearchEngine",
        "URL": SHEER_ELASTICSEARCH_SERVER,
        "INDEX_NAME": os.environ.get(
            "HAYSTACK_ELASTICSEARCH_INDEX",
            SHEER_ELASTICSEARCH_INDEX + "_haystack",
        ),
        "INCLUDE_SPELLING": True,
    }
}

ELASTICSEARCH_INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["haystack_ngram"],
                },
                "edgengram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["haystack_edgengram"],
                },
                "synonym_en": {
                    "tokenizer": "standard",
                    "filter": ["synonyms_en"],
                },
                "synonym_es": {
                    "tokenizer": "standard",
                    "filter": ["synonyms_es"],
                },
            },
            "tokenizer": {
                "haystack_ngram_tokenizer": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15,
                },
                "haystack_edgengram_tokenizer": {
                    "type": "edgeNGram",
                    "min_gram": 3,
                    "max_gram": 15,
                    "token_chars": [ "letter", "digit" ]
                },
            },
            "filter": {
                "haystack_ngram": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15,
                },
                "haystack_edgengram": {
                    "type": "edgeNGram",
                    "min_gram": 3,
                    "max_gram": 15,
                },
                "synonyms_en": {
                    "type": "synonym",
                    "synonyms_path": "analysis/synonyms_en.txt",
                },
                "synonyms_es": {
                    "type": "synonym",
                    "synonyms_path": "analysis/synonyms_es.txt",
                },
            },
        }
    }
}

ELASTICSEARCH_DEFAULT_ANALYZER = "snowball"

# ElasticSearch 7 Configuration
if os.environ.get('USE_AWS_ES', False):
    awsauth = AWS4Auth(
        os.environ.get('AWS_ES_ACCESS_KEY'),
        os.environ.get('AWS_ES_SECRET_KEY'),
        'us-east-1',
        'es'
    )
    host = os.environ.get('ES7_HOST', '')
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': [{'host': host, 'port': 443}],
            'http_auth': awsauth,
            'use_ssl': True,
            'connection_class': RequestsHttpConnection
        },
    }
else:
    host = os.environ.get("ES7_HOST", "localhost")
    port = os.environ.get("ES_PORT", "9200")
    ELASTICSEARCH_DSL = {
        "default": {"hosts": f"http://{host}:{port}"}
    }

# S3 Configuration
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_LOCATION = "f"  # A path prefix that will be prepended to all uploads
AWS_QUERYSTRING_AUTH = False  # do not add auth-related query params to URL
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SECURE_URLS = True  # True = use https; False = use http
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = None  # Default to using the ACL of the bucket

if os.environ.get("S3_ENABLED", "False") == "True":
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    if os.environ.get("AWS_S3_CUSTOM_DOMAIN"):
        AWS_S3_CUSTOM_DOMAIN = os.environ["AWS_S3_CUSTOM_DOMAIN"]
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    MEDIA_URL = os.path.join(os.environ.get("AWS_S3_URL"), AWS_LOCATION, "")


# GovDelivery
GOVDELIVERY_ACCOUNT_CODE = os.environ.get("GOVDELIVERY_ACCOUNT_CODE")

# Removes wagtail version update check banner from admin page
WAGTAIL_ENABLE_UPDATE_CHECK = False

# Email
ADMINS = admin_emails(os.environ.get("ADMIN_EMAILS"))

if DEPLOY_ENVIRONMENT:
    EMAIL_SUBJECT_PREFIX = "[{}] ".format(DEPLOY_ENVIRONMENT.title())

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = os.environ.get(
    "WAGTAILADMIN_NOTIFICATION_FROM_EMAIL"
)


# Password Policies
# cfpb_common password rules
CFPB_COMMON_PASSWORD_RULES = [
    [r".{12,}", "Minimum allowed length is 12 characters"],
    [r"[A-Z]", "Password must include at least one capital letter"],
    [r"[a-z]", "Password must include at least one lowercase letter"],
    [r"[0-9]", "Password must include at least one digit"],
    [
        r"[@#$%&!]",
        "Password must include at least one special character (@#$%&!)",
    ],
]
# cfpb_common login rules
# in seconds
LOGIN_FAIL_TIME_PERIOD = os.environ.get("LOGIN_FAIL_TIME_PERIOD", 120 * 60)
# number of failed attempts
LOGIN_FAILS_ALLOWED = os.environ.get("LOGIN_FAILS_ALLOWED", 5)
LOGIN_REDIRECT_URL = "/admin/"
LOGIN_URL = "/login/"

# When we generate an full HTML version of the regulation, we want to
# write it out somewhere. This is where.
OFFLINE_OUTPUT_DIR = ""

DATE_FORMAT = "n/j/Y"

GOOGLE_ANALYTICS_ID = ""
GOOGLE_ANALYTICS_SITE = ""

# Regulations.gov environment variables
REGSGOV_BASE_URL = os.environ.get("REGSGOV_BASE_URL")
REGSGOV_API_KEY = os.environ.get("REGSGOV_API_KEY")

# CDNs
WAGTAILFRONTENDCACHE = {}

ENABLE_AKAMAI_CACHE_PURGE = os.environ.get("ENABLE_AKAMAI_CACHE_PURGE", False)
if ENABLE_AKAMAI_CACHE_PURGE:
    WAGTAILFRONTENDCACHE["akamai"] = {
        "BACKEND": "v1.models.caching.AkamaiBackend",
        "CLIENT_TOKEN": os.environ.get("AKAMAI_CLIENT_TOKEN"),
        "CLIENT_SECRET": os.environ.get("AKAMAI_CLIENT_SECRET"),
        "ACCESS_TOKEN": os.environ.get("AKAMAI_ACCESS_TOKEN"),
    }

ENABLE_CLOUDFRONT_CACHE_PURGE = os.environ.get(
    "ENABLE_CLOUDFRONT_CACHE_PURGE", False
)
if ENABLE_CLOUDFRONT_CACHE_PURGE:
    WAGTAILFRONTENDCACHE["files"] = {
        "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudfrontBackend",
        "DISTRIBUTION_ID": {
            "files.consumerfinance.gov": os.environ.get(
                "CLOUDFRONT_DISTRIBUTION_ID_FILES"
            )
        },
    }

# CSP Allowlists

# These specify what is allowed in <script> tags
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "*.consumerfinance.gov",
    "*.google-analytics.com",
    "*.googletagmanager.com",
    "tagmanager.google.com",
    "optimize.google.com",
    "ajax.googleapis.com",
    "search.usa.gov",
    "api.mapbox.com",
    "js-agent.newrelic.com",
    "dnn506yrbagrg.cloudfront.net",
    "bam.nr-data.net",
    "*.youtube.com",
    "*.ytimg.com",
    "trk.cetrk.com",
    "universal.iperceptions.com",
    "cdn.mouseflow.com",
    "n2.mouseflow.com",
    "us.mouseflow.com",
    "geocoding.geo.census.gov",
    "tigerweb.geo.census.gov",
    "about:",
    "connect.facebook.net",
    "www.federalregister.gov",
    "storage.googleapis.com",
    "*.qualtrics.com",
)

# These specify valid sources of CSS code
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "*.consumerfinance.gov",
    "fast.fonts.net",
    "tagmanager.google.com",
    "optimize.google.com",
    "api.mapbox.com",
    "fonts.googleapis.com",
)

# These specify valid image sources
CSP_IMG_SRC = (
    "'self'",
    "*.consumerfinance.gov",
    "www.ecfr.gov",
    "s3.amazonaws.com",
    "www.gstatic.com",
    "ssl.gstatic.com",
    "stats.g.doubleclick.net",
    "img.youtube.com",
    "*.google-analytics.com",
    "trk.cetrk.com",
    "searchstats.usa.gov",
    "gtrk.s3.amazonaws.com",
    "*.googletagmanager.com",
    "tagmanager.google.com",
    "maps.googleapis.com",
    "optimize.google.com",
    "api.mapbox.com",
    "*.tiles.mapbox.com",
    "stats.search.usa.gov",
    "blob:",
    "data:",
    "www.facebook.com",
    "www.gravatar.com",
    "*.qualtrics.com",
)

# These specify what URL's we allow to appear in frames/iframes
CSP_FRAME_SRC = (
    "'self'",
    "*.consumerfinance.gov",
    "*.googletagmanager.com",
    "*.google-analytics.com",
    "optimize.google.com",
    "www.youtube.com",
    "*.doubleclick.net",
    "universal.iperceptions.com",
    "www.facebook.com",
    "staticxx.facebook.com",
    "mediasite.yorkcast.com",
    "*.qualtrics.com",
)

# These specify where we allow fonts to come from
CSP_FONT_SRC = (
    "'self'",
    "data:",
    "*.consumerfinance.gov",
    "fast.fonts.net",
    "fonts.google.com",
    "fonts.gstatic.com",
)

# These specify hosts we can make (potentially) cross-domain AJAX requests to
CSP_CONNECT_SRC = (
    "'self'",
    "*.consumerfinance.gov",
    "*.google-analytics.com",
    "*.tiles.mapbox.com",
    "api.mapbox.com",
    "bam.nr-data.net",
    "s3.amazonaws.com",
    "public.govdelivery.com",
    "n2.mouseflow.com",
    "api.iperceptions.com",
    "*.qualtrics.com",
)

# These specify valid media sources (e.g., MP3 files)
CSP_MEDIA_SRC = (
    "'self'",
    "*.consumerfinance.gov",
)

# Feature flags
# All feature flags must be listed here with a dict of any hard-coded
# conditions or an empty dict. If the conditions dict is empty the flag will
# only be enabled if database conditions are added.
FLAGS = {
    # Ask CFPB search spelling correction support
    # When enabled, spelling suggestions will appear in Ask CFPB search and
    # will be used when the given search term provides no results
    "ASK_SEARCH_TYPOS": [],
    # Ask CFPB date label
    # When enabled, date label will be changed from 'updated' to 'last reviewed'
    "ASK_UPDATED_DATE_LABEL": [],
    # Beta banner, seen on beta.consumerfinance.gov
    # When enabled, a banner appears across the top of the site proclaiming
    # "This beta site is a work in progress."
    "BETA_NOTICE": [("environment is", "beta")],
    # When enabled, include a recruitment code comment in the base template
    "CFPB_RECRUITING": [],
    # When enabled, display a "technical issues" banner on /complaintdatabase
    "CCDB_TECHNICAL_ISSUES": [],
    # When enabled, display a banner stating the complaint intake form is down
    "COMPLAINT_INTAKE_TECHNICAL_ISSUES": [
        {
            "condition": "path matches",
            "value": r"^/complaint",
            "required": True,
        },
        # Boolean to turn it off explicitly unless enabled by another condition
        {"condition": "boolean", "value": False},
    ],
    # When enabled, display a banner stating that the complaint intake form is
    # offline for maintenance. A combination of 'after date'/'before date'
    # conditions is expected.
    "COMPLAINT_INTAKE_MAINTENANCE": [
        {
            "condition": "path matches",
            "value": r"^/complaint",
            "required": True,
        },
        # Boolean to turn it off explicitly unless enabled by another condition
        {"condition": "boolean", "value": False},
    ],
    # Fix for margin-top when using the text inset
    # When enabled, the top margin of full-width text insets is increased
    "INSET_TEST": [],
    # The next version of the public consumer complaint database
    "CCDB5_RELEASE": [],
    # The Trends feature inside Consumer Complaints
    "CCDB5_TRENDS": [],
    # Google Optimize code snippets for A/B testing
    # When enabled this flag will add various Google Optimize code snippets.
    # Intended for use with path conditions.
    "AB_TESTING": [],
    # Email popups.
    "EMAIL_POPUP_OAH": [("boolean", True)],
    "EMAIL_POPUP_DEBT": [("boolean", True)],
    # Search.gov API-based site-search
    "SEARCH_DOTGOV_API": [],
    # Turbolinks is a JS library that speeds up page loads
    # https://github.com/turbolinks/turbolinks
    "TURBOLINKS": [],
    # Ping google on page publication in production only
    "PING_GOOGLE_ON_PUBLISH": [("environment is", "production")],
    # SPLIT TESTING FLAGS
    # Ask CFPB page titles as H1s instead of H2s
    "ASK_CFPB_H1": [("in split testing cluster", "ASK_CFPB_H1")],
    # Manually enabled when Beta is being used for an external test.
    # Controls the /beta_external_testing endpoint, which Jenkins jobs
    # query to determine whether to refresh Beta database.
    "BETA_EXTERNAL_TESTING": [],
    # Used to hide new youth employment success pages prior to public launch
    "YOUTH_EMPLOYMENT_SUCCESS": [],
    # Used to hide CCDB landing page updates prior to public launch
    "CCDB_CONTENT_UPDATES": [],
    # During a Salesforce system outage, the following flag should be enabled
    # to alert users that the Collect community is down.
    "COLLECT_OUTAGE": [
        {
            "condition": "path matches",
            "value": (
                r"^/data-research/credit-card-data/terms-credit-card-plans-survey/$|"  # noqa: E501
                r"^/data-research/prepaid-accounts/$"
            ),
            "required": True,
        },
        # Boolean to turn it off explicitly unless enabled by another condition
        {"condition": "boolean", "value": False},
    ],
    # During a Salesforce system outage, the following flag
    # should be enabled to alert users that
    # the OMWI assessment form and inclusivity portal are down.
    "OMWI_SALESFORCE_OUTAGE": [
        {
            "condition": "path matches",
            "value": (
                r"^/about-us/diversity-and-inclusion/$|"
                r"^/about-us/diversity-and-inclusion/self-assessment-financial-institutions/$"
            ),  # noqa: E501
            "required": True,
        },
        # Boolean to turn it off explicitly unless enabled by another condition
        {"condition": "boolean", "value": False},
    ],
    # Controls whether or not to include Qualtrics Web Intercept code for the
    # Q42020 Ask CFPB customer satisfaction survey.
    "ASK_SURVEY_INTERCEPT": [],
}


# Watchman tokens, used to authenticate global status endpoint
WATCHMAN_TOKENS = os.environ.get("WATCHMAN_TOKENS", os.urandom(32))

# This specifies what checks Watchman should run and include in its output
# https://github.com/mwarkentin/django-watchman#custom-checks
WATCHMAN_CHECKS = (
    "watchman.checks.databases",
    "watchman.checks.storage",
    "watchman.checks.caches",
    "alerts.checks.check_clock_drift",
)

# Used to check server's time against in check_clock_drift
NTP_TIME_SERVER = "north-america.pool.ntp.org"

# If server's clock drifts from NTP by more than specified offset
# (in seconds), check_clock_drift will fail
MAX_ALLOWED_TIME_OFFSET = 5

# Search.gov values
SEARCH_DOT_GOV_AFFILIATE = os.environ.get("SEARCH_DOT_GOV_AFFILIATE")
SEARCH_DOT_GOV_ACCESS_KEY = os.environ.get("SEARCH_DOT_GOV_ACCESS_KEY")

# We want the ability to serve the latest drafts of some pages on beta
# This value is read by v1.wagtail_hooks
SERVE_LATEST_DRAFT_PAGES = []

# To expose a previously-published page's latest draft version on beta,
# add its primary key to the list below
if DEPLOY_ENVIRONMENT == "beta":
    SERVE_LATEST_DRAFT_PAGES = []

# Email popup configuration. See v1.templatetags.email_popup.
EMAIL_POPUP_URLS = {
    "debt": [
        "/ask-cfpb/what-is-a-statute-of-limitations-on-a-debt-en-1389/",
        "/ask-cfpb/what-is-the-best-way-to-negotiate-a-settlement-with-a-debt-collector-en-1447/",  # noqa 501
        "/ask-cfpb/what-should-i-do-when-a-debt-collector-contacts-me-en-1695/",  # noqa 501
        "/consumer-tools/debt-collection/",
    ],
    "oah": ["/owning-a-home/", "/owning-a-home/mortgage-estimate/"],
}

REGULATIONS_REFERENCE_MAPPING = [
    (
        r"(?P<section>[\w]+)-(?P<paragraph>[\w-]*-Interp)",
        "Interp-{section}",
        "{section}-{paragraph}",
    ),
]


# See core.middleware.ParseLinksMiddleware. Normally all HTML responses get
# processed by this middleware so that their link content gets the proper
# markup (e.g., download icons). We want to exclude certain pages from this
# middleware. This list of regular expressions defines a set of URLs against
# which we don't want this logic to be run.
PARSE_LINKS_EXCLUSION_LIST = [
    # Wagtail admin pages, except preview, draft, and debug views
    (
        r"^/admin/(?!"
        r"pages/\d+/(edit/preview|view_draft)/|"
        r"mega_menu/menu/preview/\w+/|"
        r"template_debug/"
        r")"
    ),
    # Django admin pages
    r"^/django-admin/",
    # Our custom login pages
    r"^/login/",
    # Regulations pages that have their own link markup
    r"^/policy-compliance/rulemaking/regulations/\d+/",
]

# Required by django-extensions to determine the execution directory used by
# scripts executed with the "runscript" management command
# See https://django-extensions.readthedocs.io/en/latest/runscript.html
BASE_DIR = "scripts"

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "h2",
                "h3",
                "h4",
                "h5",
                "blockquote",
                "hr",
                "ol",
                "ul",
                "bold",
                "italic",
                "link",
                "document-link",
                "image",
            ]
        },
    },
}
