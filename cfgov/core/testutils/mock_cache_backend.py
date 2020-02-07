try:
    from wagtail.contrib.frontend_cache.backends import BaseBackend
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.contrib.wagtailfrontendcache.backends import BaseBackend


CACHE_PURGED_URLS = []


class MockCacheBackend(BaseBackend):
    def __init__(self, config):
        pass

    def purge(self, url):
        CACHE_PURGED_URLS.append(url)
