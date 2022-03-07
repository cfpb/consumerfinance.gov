from fnmatch import fnmatch

from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder, get_finders
from django.core.exceptions import ImproperlyConfigured


class MockStaticfilesFinder(BaseFinder):
    """A Django Staticfiles finder backend that mocks certain files.

    This finder replaces requests for certain static files that don't exist
    with other static files that do.

    Depends on a MOCK_STATICFILES_PATTERNS setting that must contain a list of
    patterns to match and files to serve instead when those patterns are
    requested. Replacement files must be patterns that could ordinarily be
    served successfully by another staticfiles finder.

    For example, given this setting:

    MOCK_STATICFILES_PATTERNS = {
        'file.txt': 'some/other/file.txt',
        'path/to/images/*.jpg': 'some/other/image.jpg',
    }

    then a request to static('file.txt') that might otherwise fail (if not
    provided by other staticfiles finders) will instead delegate to a request
    to static('some/other/file.txt'). Similarly, a request that matches a
    wildcard, like static('path/to/images/foo.jpg') will be delegated to a
    request to static('some/other/image.jpg').

    If a given path matches more than one pattern, the replacement used is not
    guaranteed due to unpredictable dict sorting order.

    Warning: the Django docs currently say that "Static file finders are
    currently considered a private interface, and this interface is thus
    undocumented." Use at your own risk.
    """

    setting = "MOCK_STATICFILES_PATTERNS"

    @property
    def patterns(self):
        try:
            patterns = getattr(settings, self.setting)
        except AttributeError:
            raise ImproperlyConfigured(
                "settings.{} must be defined".format(self.setting)
            )

        if not isinstance(patterns, dict):
            raise ImproperlyConfigured(
                "settings.{} must be a dict".format(self.setting)
            )

        return patterns

    def find(self, path, all=False):
        for pattern, replacement in self.patterns.items():
            if not fnmatch(path, pattern):
                continue

            result = self._find_in_other_finders(replacement, all=all)

            if result:
                return result

        return []

    def _find_in_other_finders(self, path, all=False):
        """Look for one or more matches in finders besides this one.

        Unfortunately much of this logic has to be duplicated from
        django.contrib.staticfiles.finders.find, because there's no easy way
        to eliminate this finder from the search and avoid infinite recusion.
        """
        matches = []

        for finder in get_finders():
            if isinstance(finder, self.__class__):
                continue

            result = finder.find(path, all=all)

            if not all and result:
                return result

            if not isinstance(result, (list, tuple)):
                result = [result]

            matches.extend(result)

        return matches

    def list(self, ignore_patterns):
        return []
