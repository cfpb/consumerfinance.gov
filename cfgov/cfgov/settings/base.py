import os
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import dj_database_url

from cfgov.util import admin_emails, environment_json, get_s3_media_config


# Repository root is 4 levels above this file
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

# This is the root of the Django project, 'cfgov'
PROJECT_ROOT = REPOSITORY_ROOT.joinpath("cfgov")

# Templates that are not scoped to specific Django apps will live here
GLOBAL_TEMPLATE_ROOT = PROJECT_ROOT.joinpath("jinja2")

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

# Application definition
INSTALLED_APPS = (
    "permissions_viewer",
    "wagtail",
    "wagtailadmin_overrides",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.images",
    "wagtail.embeds",
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.redirects",
    "wagtail.contrib.forms",
    "wagtail.sites",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.typed_table_block",
    "wagtail.contrib.settings",
    "localflavor",
    "modelcluster",
    "taggit",
    "dal",
    "dal_select2",
    "wagtailinventory",
    "wagtailsharing",
    "flags",
    "wagtailautocomplete",
    "wagtailflags",
    "ask_cfpb",
    "agreements",
    "searchgov",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    # Including WhiteNoise before staticfiles so that WhiteNoise always
    # serves static files, even in development.
    # https://whitenoise.readthedocs.io/en/latest/django.html#using-whitenoise-in-development
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "wagtail.search",
    "storages",
    "data_research",
    "v1",
    "cdntools",
    "core",
    "django_extensions",
    "jobmanager",
    "wellbeing",
    "search",
    "paying_for_college",
    "prepaid_agreements",
    "regulations3k",
    "retirement_api",
    "treemodeladmin",
    "housing_counselor",
    "hmda",
    "diversity_inclusion",
    "privacy",
    "mega_menu.apps.MegaMenuConfig",
    "form_explainer.apps.FormExplainerConfig",
    "teachers_digital_platform",
    "django_opensearch_dsl",
    "corsheaders",
    "login",
    "login.apps.LoginUsersAppConfig",
    "filing_instruction_guide",
    "health_check",
    "health_check.db",
    "wagtailcharts",
    # Satellites
    "complaint_search",
    "countylimits",
    "mptt",
    "ratechecker",
    "rest_framework",
    "wagtail_modeladmin",
    "wagtail_draftail_anchors",
    "django_filters",
    "django_htmx",
    "wagtail_content_audit",
    "mozilla_django_oidc",
    "draftail_icons",
    "wagtail_footnotes",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.PathBasedCsrfViewMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "core.middleware.ParseLinksMiddleware",
    "core.middleware.DownstreamCacheControlMiddleware",
    "core.middleware.SelfHealingMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "core.middleware.DeactivateTranslationsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

CSP_MIDDLEWARE = ("csp.middleware.CSPMiddleware",)

if "CSP_ENFORCE" in os.environ:
    MIDDLEWARE += CSP_MIDDLEWARE

ROOT_URLCONF = "cfgov.urls"

# We support two different template engines: Django templates and Jinja2
# templates. See https://docs.djangoproject.com/en/stable/topics/templates/
# for an overview of how Django templates work.

wagtail_extensions = [
    "wagtail.jinja2tags.core",
    "wagtail.admin.jinja2tags.userbar",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Look for Django templates in each app under a templates subdirectory
        "APP_DIRS": True,
        "OPTIONS": {
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
            GLOBAL_TEMPLATE_ROOT,
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
                "core.jinja2tags.language",
                "agreements.jinja2tags.agreements",
                "mega_menu.jinja2tags.MegaMenuExtension",
                "prepaid_agreements.jinja2tags.prepaid_agreements",
                "regulations3k.jinja2tags.regulations",
                "v1.jinja2tags.datetimes_extension",
                "v1.jinja2tags.images_extension",
                "v1.jinja2tags.v1_extension",
            ],
        },
    },
]

WSGI_APPLICATION = "cfgov.wsgi.application"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000  # For heavy Wagtail pages

# Default database is PostgreSQL running on localhost.
# Database name cfgov, username cfpb, password cfpb.
# Override this by setting DATABASE_URL in the environment.
# See https://github.com/jazzband/dj-database-url for URL formatting.
_db_config = {
    "default": "postgres://cfpb:cfpb@localhost/cfgov",
}

if _db_conn_max_age := os.getenv("CONN_MAX_AGE"):
    _db_config.update({
        "conn_max_age": int(_db_conn_max_age),
        "conn_health_checks": True,
    })

DATABASES = {
    "default": dj_database_url.config(**_db_config)
}

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
    ("zh-Hant", _("Chinese")),
    ("vi", _("Vietnamese")),
    ("ko", _("Korean")),
    ("tl", _("Tagalog")),
    ("ru", _("Russian")),
    ("ar", _("Arabic")),
    ("ht", _("Haitian Creole")),
)

# Add the Django project cfgov/cfgov/locale/ directory to LOCALE_PATHS.
# This will make the search order: cfgov/locale then APP/locale for every APP
# in INSTALLED_APPS.
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, "cfgov", "locale"),)

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

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

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Add the frontend build output to static files.
STATICFILES_DIRS = [
    PROJECT_ROOT.joinpath("static_built"),
]

# Also include any directories under static.in
STATICFILES_DIRS += [
    d for d in REPOSITORY_ROOT.joinpath("static.in").iterdir() if d.is_dir()
]

# Collect static files into, and serve them from, cfgov/collectstatic,
# unless otherwise specified via DJANGO_STATIC_ROOT.
STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", REPOSITORY_ROOT / "collectstatic")

# Serve files under cfgov/root at the root of the website.
WHITENOISE_ROOT = PROJECT_ROOT / "root"

# To be overridden by other settings files.
ALLOWED_HOSTS = []

# Wagtail settings
WAGTAIL_SITE_NAME = "consumerfinance.gov"
WAGTAILIMAGES_IMAGE_MODEL = "v1.CFGOVImage"
WAGTAILIMAGES_IMAGE_FORM_BASE = "v1.forms.CFGOVImageForm"
TAGGIT_CASE_INSENSITIVE = True
WAGTAILDOCS_SERVE_METHOD = "direct"

# This is used for easy autocomplete search behavior in the Wagtail admin.
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database.fallback",
    }
}

# This is the name of the template that will render a footnote citaiton
# inline in rich text.
WAGTAIL_FOOTNOTES_REFERENCE_TEMPLATE = "v1/includes/rich-text/footnote-reference.html"

# Search api
SEARCHGOV_API_KEY = os.environ.get("SEARCHGOV_API_KEY")
SEARCHGOV_ES_API_KEY = os.environ.get("SEARCHGOV_ES_API_KEY")

# LEGACY APPS
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")

# OpenSearch configuration
ES_SCHEMA = os.getenv("ES_SCHEMA", "http")
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", "9200")

OPENSEARCH_BIGINT = 50000
OPENSEARCH_DEFAULT_ANALYZER = "snowball"
OPENSEARCH_DSL = {
    "default": {
        "hosts": f"{ES_SCHEMA}://{ES_HOST}:{ES_PORT}",
        "http_auth": (
            os.getenv("ES_USER", "admin"),
            os.getenv("ES_PASS", "admin"),
        ),
        "use_ssl": True,
        "verify_certs": not os.getenv("OPENSEARCH_DSL_SKIP_CERT_VERIFICATION"),
    }
}

OPENSEARCH_DSL_SIGNAL_PROCESSOR = (
    "search.elasticsearch_helpers.WagtailSignalProcessor"
)

if os.getenv("S3_ENABLED"):
    MEDIA_URL, _storage_options = get_s3_media_config()
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": _storage_options,
    }

# These environment variables are also used in get_s3_media_config above.
# They are defined here to maintain existing functionality
# in various applications that read/write data from/to S3.
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", "files.consumerfinance.gov")

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
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = False

PRIVACY_EMAIL_TARGET = os.environ.get("PRIVACY_EMAIL_TARGET", "test@localhost")

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# Password Policies
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 14,
        },
    },
    {
        "NAME": "login.password_validation.PasswordRegexValidator",
        "OPTIONS": {
            "regex": r"[A-Z]",
            "message": "Password must include at least one capital letter.",
        },
    },
    {
        "NAME": "login.password_validation.PasswordRegexValidator",
        "OPTIONS": {
            "regex": r"[a-z]",
            "message": "Password must include at least one lowercase letter.",
        },
    },
    {
        "NAME": "login.password_validation.PasswordRegexValidator",
        "OPTIONS": {
            "regex": r"[0-9]",
            "message": "Password must include at least one digit.",
        },
    },
    {
        "NAME": "login.password_validation.PasswordRegexValidator",
        "OPTIONS": {
            "regex": r"[@#$%&!]",
            "message": "Password must include at least one special character (@#$%&!).",
        },
    },
]

DATE_FORMAT = "n/j/Y"

# CDNs
WAGTAILFRONTENDCACHE = {}

ENABLE_AKAMAI_CACHE_PURGE = os.environ.get("ENABLE_AKAMAI_CACHE_PURGE", False)
if ENABLE_AKAMAI_CACHE_PURGE:
    WAGTAILFRONTENDCACHE["akamai"] = {
        "BACKEND": "cdntools.backends.AkamaiBackend",
        "CLIENT_TOKEN": os.environ["AKAMAI_CLIENT_TOKEN"],
        "CLIENT_SECRET": os.environ["AKAMAI_CLIENT_SECRET"],
        "ACCESS_TOKEN": os.environ["AKAMAI_ACCESS_TOKEN"],
        "PURGE_ALL_URL": os.environ["AKAMAI_PURGE_ALL_URL"],
        "FAST_PURGE_URL": os.environ["AKAMAI_FAST_PURGE_URL"],
        # Unique to www cache
        "OBJECT_ID": os.environ["AKAMAI_OBJECT_ID"],
        "HOSTNAMES": environment_json("AKAMAI_PURGE_HOSTNAMES")
    }

ENABLE_FILES_CACHE_PURGE = os.environ.get(
    "ENABLE_FILES_CACHE_PURGE", False
)
if ENABLE_FILES_CACHE_PURGE:
    WAGTAILFRONTENDCACHE["files"] = {
        "BACKEND": "cdntools.backends.AkamaiBackend",
        "CLIENT_TOKEN": os.environ["AKAMAI_CLIENT_TOKEN"],
        "CLIENT_SECRET": os.environ["AKAMAI_CLIENT_SECRET"],
        "ACCESS_TOKEN": os.environ["AKAMAI_ACCESS_TOKEN"],
        "PURGE_ALL_URL": os.environ["AKAMAI_PURGE_ALL_URL"],
        "FAST_PURGE_URL": os.environ["AKAMAI_FAST_PURGE_URL"],
        # Unique to files cache
        "OBJECT_ID": os.environ["AKAMAI_FILES_OBJECT_ID"],
        "HOSTNAMES": environment_json("AKAMAI_FILES_PURGE_HOSTNAMES")
    }

# CSP Allowlists
#
# Please note: Changing these lists will change the value of the
# Content-Security-Policy header Django returns. Django does NOT include
# header values when calculating the response hash returned in the ETag
# header.
# Our Akamai cache uses the ETag header to know whether a cached copy of a
# page has been updated after it expires or after an invalidation purge.
#
# Together, this means that any changes to these CSP values WILL NOT BE
# RETURNED by Akamai until a page's non-header content changes, or a
# delete-purge is performed.

# These specify what is allowed in <script> tags
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "*.consumerfinance.gov",
    "dap.digitalgov.gov",
    "*.googleanalytics.com",
    "*.google-analytics.com",
    "*.googletagmanager.com",
    "api.mapbox.com",
    "js-agent.newrelic.com",
    "bam.nr-data.net",
    "gov-bam.nr-data.net",
    "*.youtube.com",
    "*.ytimg.com",
    "*.mouseflow.com",
    "*.geo.census.gov",
    "about:",
    "www.federalregister.gov",
    "*.qualtrics.com",
    "www.ssa.gov/accessibility/andi/",
    "ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js", # needed for ANDI accessibility tool
)

# These specify valid sources of CSS code
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "*.consumerfinance.gov",
    "*.googletagmanager.com",
    "fonts.googleapis.com",
    "api.mapbox.com",
    "www.ssa.gov/accessibility/andi/",
)

# These specify valid image sources
CSP_IMG_SRC = (
    "'self'",
    "*.cfpb.gov",
    "*.consumerfinance.gov",
    "www.ecfr.gov",
    "s3.amazonaws.com",
    "img.youtube.com",
    "*.google-analytics.com",
    "*.googletagmanager.com",
    "api.mapbox.com",
    "*.tiles.mapbox.com",
    "blob:",
    "data:",
    "www.gravatar.com",
    "*.qualtrics.com",
    "*.mouseflow.com",
    "i.ytimg.com",
    "www.ssa.gov/accessibility/andi/",
)

# These specify what URL's we allow to appear in frames/iframes
CSP_FRAME_SRC = (
    "'self'",
    "*.consumerfinance.gov",
    "*.googletagmanager.com",
    "*.google-analytics.com",
    "www.youtube.com",
    "*.qualtrics.com",
    "mailto:",
)

# These specify where we allow fonts to come from
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com")

# These specify hosts we can make (potentially) cross-domain AJAX requests to
CSP_CONNECT_SRC = (
    "'self'",
    "*.consumerfinance.gov",
    "dap.digitalgov.gov",
    "*.google-analytics.com",
    "*.tiles.mapbox.com",
    "api.mapbox.com",
    "bam.nr-data.net",
    "gov-bam.nr-data.net",
    "s3.amazonaws.com",
    "public.govdelivery.com",
    "*.mouseflow.com",
    "*.qualtrics.com",
    "raw.githubusercontent.com",
)

# These specify valid media sources (e.g., MP3 files)
CSP_MEDIA_SRC = (
    "'self'",
    "*.consumerfinance.gov",
)

# FEATURE FLAGS
# Flags can be declared here with an empty list, which will evaluate as false
# until the flag is enabled in the Wagtail admin, or with a list of conditions.
# Each condition should be a tuple or dict in one of these forms:
# (condition-string, value) or {"condition": condition-string, "value": value}
# An optional 3rd value, "required," can be set to True. It defaults to False.
# Flags can also be created (and deleted) in the Wagtail admin.
FLAGS = {
    # Ask CFPB search spelling correction support
    # When enabled, spelling suggestions will appear in Ask CFPB search and
    # will be used when the given search term provides no results
    "ASK_SEARCH_TYPOS": [],
    # Beta banner, seen on beta.consumerfinance.gov
    # When enabled, a banner appears across the top of the site proclaiming
    # "This beta site is a work in progress."
    "BETA_NOTICE": [("environment is", "beta")],
    # When enabled, include a recruitment code comment in the base template
    "CFPB_RECRUITING": [],
    # When enabled, display a "technical issues" banner on /complaintdatabase
    "CCDB_TECHNICAL_ISSUES": [],
    # Manually enabled when Beta is being used for an external test.
    # Controls the /beta_external_testing endpoint, which Jenkins jobs
    # query to determine whether to refresh Beta database.
    "BETA_EXTERNAL_TESTING": [],
    # Controls whether or not to include Qualtrics Web Intercept code
    "PATH_MATCHES_FOR_QUALTRICS": [],
    # Whether robots.txt should block all robots, except for Search.gov.
    "ROBOTS_TXT_SEARCH_GOV_ONLY": [("environment is", "beta")],
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
    # DjangoRestFramework API pages where link icons are intrusive
    r"^/oah-api/",
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
                "anchor-identifier",
                "h2",
                "h3",
                "h4",
                "h5",
                "hr",
                "ol",
                "ul",
                "bold",
                "italic",
                "superscript",
                "blockquote",
                "link",
                "document-link",
                "image",
                "icon",
            ]
        },
    },
}

# Serialize Decimal(3.14) as 3.14, not "3.14"
REST_FRAMEWORK = {"COERCE_DECIMAL_TO_STRING": False}

# We require CSRF only on authenticated paths. This setting is handled by our
# core.middleware.PathBasedCsrfViewMiddleware.
#
# Any paths listed here that are public-facing will receive an "
# "Edge-Control: no-store" header from our
# core.middleware.DownstreamCacheControlMiddleware and will not be cached.
CSRF_REQUIRED_PATHS = (
    "/login",
    "/admin",
    "/django-admin",
)

# Cache Settings
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cfgov_default_cache",
        "TIMEOUT": None,
    },
}

# Set our CORS allowed origins based on a JSON list in the
# CORS_ALLOWED_ORIGINS environment variable.
CORS_ALLOWED_ORIGINS = environment_json(
    "CORS_ALLOWED_ORIGINS",
    (
        "Environment variable CORS_ALLOWED_ORIGINS is not valid JSON. "
        "Expected a JSON array of allowed origins."
    ),
    default="[]",
)

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.getenv(
    "WAGTAILADMIN_BASE_URL", "http://localhost:8000"
)

DRAFTAIL_ANCHORS_RENDERER = "wagtail_draftail_anchors.rich_text.render_span"

# Two abbreviations to note:
# - OP indicates the OIDC identity provider
# - RP indicates the OIDC relying party, the client, this application
#
# Requires the following environment variables to be defined:
#
# - ENABLE_SSO: Enables SSO authentication if defined.
# - OIDC_RP_CLIENT_ID: OIDC client identifier provided by the OP
# - OIDC_RP_CLIENT_SECRET: OIDC client secret provided by the OP
# - OIDC_RP_SIGN_ALGO: The algorithm used to sign ID tokens
#
# Endpoints on the OIDC provider (with typical last path components):
# - OIDC_OP_AUTHORIZATION_ENDPOINT: authorization endpoint (/authorize)
# - OIDC_OP_TOKEN_ENDPOINT: token endpoint (/token)
# - OIDC_OP_USER_ENDPOINT: userinfo endpoint (/userinfo)
# - OIDC_OP_JWKS_ENDPOINT: JWKS endpoint (alternative to OIDC_RP_IDP_SIGN_KEY)
#
# Optional environment variables:
# - OIDC_RP_IDP_SIGN_KEY: The key (PEM) to sign ID tokens when
#                         OIDC_RP_SIGN_ALGO is RS256 (default: None)
# - OIDC_ADMIN_GROUP: The group claim for admins
#
# See the mozilla-django-oidc documentation for more details about the
# settings below:
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html
ENABLE_SSO = bool(os.environ.get("ENABLE_SSO"))
if ENABLE_SSO:
    # Add our OIDC authentication backend, a subclass of
    # mozilla_django_oidc.auth.OIDCAuthenticationBackend
    AUTHENTICATION_BACKENDS += ("login.auth.CFPBOIDCAuthenticationBackend",)

    # Add OIDC middleware that refreshes sessions from the provider
    MIDDLEWARE += ("mozilla_django_oidc.middleware.SessionRefresh",)

    # Configure login/out URLs for OIDC
    LOGIN_REDIRECT_URL = reverse_lazy("wagtailadmin_home")
    LOGOUT_REDIRECT_URL = reverse_lazy("cfgov_login")
    ALLOW_LOGOUT_GET_METHOD = True

    # Disable Wagtail password reset
    WAGTAIL_PASSWORD_RESET_ENABLED = False

    # This OIDC client's id and secret
    OIDC_RP_CLIENT_ID = os.environ["OIDC_RP_CLIENT_ID"]
    OIDC_RP_CLIENT_SECRET = os.environ["OIDC_RP_CLIENT_SECRET"]

    # The OIDC provider's signing algorithms and key/key endpoint
    OIDC_RP_SIGN_ALGO = os.environ["OIDC_RP_SIGN_ALGO"]

    # Because only one of these two values is required if
    # OIDC_RP_SIGN_ALGO="RS256", we allow them to be None, and the OIDC
    # library will raise an error if neither are defined.
    OIDC_RP_IDP_SIGN_KEY = os.environ.get("OIDC_RP_IDP_SIGN_KEY")
    OIDC_OP_JWKS_ENDPOINT = os.environ.get("OIDC_OP_JWKS_ENDPOINT")

    # OIDC provider endpoints
    OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ[
        "OIDC_OP_AUTHORIZATION_ENDPOINT"
    ]
    OIDC_OP_TOKEN_ENDPOINT = os.environ["OIDC_OP_TOKEN_ENDPOINT"]
    OIDC_OP_USER_ENDPOINT = os.environ["OIDC_OP_USER_ENDPOINT"]

    # For users created just-in-time, assign a username based on the
    # username portion of their email address.
    OIDC_USERNAME_ALGO = "login.auth.username_from_email"

    # Now we do some role/group-mapping for admins and regular users
    # Upstream "role" for users who get is_superuser
    OIDC_OP_ADMIN_ROLE = os.environ.get("OIDC_OP_ADMIN_ROLE")

    # Require manual Wagtail user creation.
    OIDC_CREATE_USER = False

if WAGTAILSHARING_HOST := os.getenv("WAGTAILSHARING_HOST"):
    WAGTAILSHARING_ROUTER = "wagtailsharing.routers.settings.SettingsHostRouter"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG" if os.getenv("ENABLE_SQL_LOGGING") else "INFO",
            "propagate": False,
        },
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

if os.getenv("ENABLE_ES_LOGGING"):
    LOGGING["loggers"]["opensearchpy.trace"] = {
        "handlers": ["console"],
        "level": "INFO",
        "propagate": False,
    }

# Opt out of Google's Federated Learning of Cohorts approach to tracking
PERMISSIONS_POLICY = {
    "interest-cohort": [],
}
