from urllib.parse import urlparse

from django.conf import settings


def url_in_archive(url) -> bool:
    """Returns boolean indicating whether a URL lives in the site archive area.

    Uses settings.ARCHIVE_BASE_PATH to determine site archive area.
    If this is set to "*", applies to all URLs.
    """
    if settings.ARCHIVE_BASE_PATH == "*":
        return True

    return urlparse(url).path.startswith(settings.ARCHIVE_BASE_PATH)
