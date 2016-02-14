from django.conf import settings
from unipath import Path


class SheerSite(object):
    def __init__(self, slug):
        self.slug = slug
        self.path = Path(settings.SHEER_SITES[slug])

    @property
    def urls(self):
        return []
