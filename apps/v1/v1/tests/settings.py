import os


ALLOWED_HOSTS = ["*"]

USE_TZ = True
SECRET_KEY = "not needed"

ROOT_URLCONF = "v1.tests.urls"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "NAME": os.environ.get("DATABASE_NAME", "v1.db"),
        "USER": os.environ.get("DATABASE_USER", None),
        "PASSWORD": os.environ.get("DATABASE_PASS", None),
        "HOST": os.environ.get("DATABASE_HOST", None),
        "TEST": {"NAME": os.environ.get("DATABASE_NAME", None)},
    },
}

WAGTAIL_APPS = (
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
    "wagtail.tests.testapp",
)
INSTALLED_APPS = (
    (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "taggit",
    )
    + WAGTAIL_APPS
    + (
        "core",
        "search",
        "flags",
        "wagtailflags",
        "wagtailinventory",
    )
)

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {"WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea"},
}
WAGTAILADMIN_RICH_TEXT_EDITORS["custom"] = {
    "WIDGET": "wagtail.tests.testapp.rich_text.CustomRichTextArea"
}

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

STATIC_ROOT = "/tmp/static/"
STATIC_URL = "/static/"

wagtail_extensions = []

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "debug": True,
        },
    },
    {
        "NAME": "wagtail-env",
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "v1.jinja2_environment.environment",
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.i18n",
                "jinja2.ext.loopcontrols",
                "wagtail.core.jinja2tags.core",
                "wagtail.admin.jinja2tags.userbar",
                "wagtail.images.jinja2tags.images",
                "flags.jinja2tags.flags",
                "v1.jinja2tags.datetimes_extension",
                "v1.jinja2tags.fragment_cache_extension",
                "v1.jinja2tags.v1_extension",
            ],
        },
    },
]

WAGTAIL_SITE_NAME = "Test Site"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.db",
    },
    "fulltext": {
        "BACKEND": "wagtail.search.backends.database",
    },
}
