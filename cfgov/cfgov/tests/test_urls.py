try:
    from django.urls import RegexURLPattern, RegexURLResolver
except ImportError:
    from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

from django.test import TestCase, override_settings

from cfgov import urls


# Whitelist is a list of *strings* that match the beginning of a regex string.
# For example, ''^admin' will match any urlpattern regex that starts with
# '^admin'.
ADMIN_URL_WHITELIST = [
    '^admin/',
    '^csp-report/',
    '^d/admin/',
    '^django-admin/',
    '^login',
    '^logout',
    '^password/',
    '^picard/',
    '^tasks/',
]


# Based on django_extensions's show_urls command.
def extract_regexes_from_urlpatterns(urlpatterns, base=''):
    """ Extract a list of all regexes from the given urlpatterns """
    regexes = []
    for p in urlpatterns:
        if isinstance(p, RegexURLPattern) or hasattr(p, '_get_callback'):
            regexes.append(base + p.regex.pattern)
        elif (isinstance(p, RegexURLResolver) or
              hasattr(p, 'url_patterns') or
              hasattr(p, '_get_url_patterns')):
            patterns = p.url_patterns
            regexes.extend(extract_regexes_from_urlpatterns(
                patterns, base + p.regex.pattern))
        else:
            raise TypeError("%s does not appear to be a urlpattern object" % p)
    return regexes


class AdminURLSTestCase(TestCase):

    def setUp(self):
        with override_settings(ALLOW_ADMIN_URL=False):
            # Reload cfgov.urls with the new ALLOW_ADMIN_URL
            reload(urls)
            without_admin = extract_regexes_from_urlpatterns(urls.urlpatterns)

        with override_settings(ALLOW_ADMIN_URL=True):
            # Reload cfgov.urls with the new ALLOW_ADMIN_URL
            reload(urls)
            with_admin = extract_regexes_from_urlpatterns(urls.urlpatterns)

        self.admin_urls = set(with_admin) - set(without_admin)

    def test_admin_url_whitelist(self):
        """ Test to ensure admin urls match our whitelist """
        non_matching_urls = [u for u in self.admin_urls
                             if not any(
                                 u.startswith(w) for w in ADMIN_URL_WHITELIST)]
        self.assertEqual(len(non_matching_urls), 0,
                         msg="Non-whitelisted admin URLs:\n\t{}\n".format(
                             ',\n\t'.join(non_matching_urls)))

    def tearDown(self):
        # Reload cfgov.urls with the default ALLOW_ADMIN_URLs
        reload(urls)
