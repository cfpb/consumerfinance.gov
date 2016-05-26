from django.contrib.staticfiles.finders import BaseFinder
from django.conf import settings

from unipath import Path

from .storage import SheerlikeStaticStorage


class SheerlikeStaticFinder(BaseFinder):

    def __init__(self):
        self.sites = settings.SHEER_SITES
        self.storages = {root: SheerlikeStaticStorage(location=root, slug=slug)
                         for slug, root in self.sites.items()}

    def find(self, path, all=False):
        matches = []
        for slug, site_path in self.sites.items():
            if path.startswith(slug):
                corrected_path = path[len(slug) + 1:]
                complete_path = Path(site_path, corrected_path)
                if complete_path.exists:
                    matches.append(complete_path)

        return matches

    def list(self, ignore_patterns):
        for slug, site_path in self.sites.items():
            storage = self.storages[site_path]
            if site_path.exists():
                for path in site_path.walk():
                    rel_path = site_path.rel_path_to(path)
                    if (rel_path.startswith('_') or
                            rel_path.startswith('.') or
                            rel_path.endswith('.html') or
                            path.isdir()):
                        continue
                    rooted_path = Path(slug, rel_path)
                    yield str(rooted_path), storage
