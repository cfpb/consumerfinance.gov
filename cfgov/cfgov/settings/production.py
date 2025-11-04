from django.core.exceptions import ImproperlyConfigured

from cfgov.settings.base import *
from cfgov.util import environment_json


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = os.getenv("EMAIL_PORT", 25)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False)
DEFAULT_FROM_EMAIL = "wagtail@cfpb.gov"

STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

# ALLOWED_HOSTS should be defined as a JSON list in the ALLOWED_HOSTS
# environment variable.
ALLOWED_HOSTS = environment_json(
    "ALLOWED_HOSTS",
    (
        "Environment variable ALLOWED_HOSTS is either not defined or is "
        "not valid JSON. Expected a JSON array of allowed hostnames."
    ),
)

# Django baseline required settings
SECURE_REFERRER_POLICY = "same-origin"
SESSION_COOKIE_SAMESITE = "Strict"
X_FRAME_OPTIONS = "SAMEORIGIN"
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_PRELOAD = True

# In production deployments SSL is never terminated at the Django application,
# so in practice Django will never receive secure requests. HTTP requests must
# always come with an "X-Forwarded-Proto: https" header if this is set to True
# or this we get into a redirect loop.
SECURE_SSL_REDIRECT = False

# Require the SECRET_KEY as an environment variable
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ImproperlyConfigured(
        "The SECRET_KEY environment variable must be set"
    )

# Secret key fallbacks that allow the rotation of the secret key.
# This environment variable should be a JSON array if fallbacks are available.
# This list is empty (no old fallback secret keys) if the environment variable
# SECRET_KEY_FALLBACKS is not set.
SECRET_KEY_FALLBACKS = environment_json(
    "SECRET_KEY_FALLBACKS",
    (
        "Environment variable SECRET_KEY_FALLBACKS is not valid JSON. "
        "Expected a JSON array of fallback secret keys."
    ),
    default="[]",
)

if ENABLE_SSO:
    # We need the OIDC identity provider to be able to send the sessionid to
    # the OIDC callback view in order to validate the OIDC state
    SESSION_COOKIE_SAMESITE = "Lax"

    LOGGING["loggers"]["mozilla_django_oidc"] = {
        "level": "INFO",
    }
