from wagtail.contrib.frontend_cache.backends import BaseBackend

CACHE_PURGED_URLS = []


class MockCacheBackend(BaseBackend):
    def __init__(self, config):
        pass

    def purge(self, url):
        CACHE_PURGED_URLS.append(url)
