from imp import reload

from django.conf.urls import url
from django.test import RequestFactory, TestCase, override_settings

import mock

from cfgov import urls


try:
    from django.urls import RegexURLPattern, RegexURLResolver
except ImportError:
    from django.core.urlresolvers import RegexURLPattern, RegexURLResolver


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


def dummy_external_site_view(request):
    pass  # pragma: no cover


urlpatterns = [
    # Needed for rendering of base template that calls reverse('external-site')
    url(r'^external-site/$', dummy_external_site_view, name='external-site'),

    urls.flagged_wagtail_only_view('MY_TEST_FLAG', r'^$'),
]


@override_settings(ROOT_URLCONF=__name__)
class FlaggedWagtailOnlyViewTests(TestCase):
    @override_settings(FLAGS={'MY_TEST_FLAG': [('boolean', True)]})
    def test_flag_set_returns_view_that_calls_wagtail_serve_view(self):
        """When flag is set, request should be routed to Wagtail.

        This test checks for text that is known to exist in the template for
        the Wagtail page that gets served from the site root.
        """
        response = self.client.get('/')
        self.assertContains(
            response,
            'U.S. government agency that makes sure banks'
        )

    @override_settings(FLAGS={'MY_TEST_FLAG': [('boolean', False)]})
    def test_flag_not_set_returns_view_that_raises_http404(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)


class HandleErrorTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('cfgov.urls.render')
    def test_handle_error_attribute_error(self, mock_render):
        mock_render.side_effect = AttributeError()
        result = urls.handle_error(404, self.factory.get('/test'))
        self.assertIn(b'This request could not be processed', result.content)
        self.assertIn(b'HTTP Error 404.', result.content)

    @mock.patch('cfgov.urls.render')
    def test_handle_error(self, mock_render):
        request = self.factory.get('/test')
        urls.handle_error(404, request)
        mock_render.assert_called_with(
            request, '404.html', context={'request': request}, status=404
        )


class TestBetaRefreshEndpoint(TestCase):
    def test_beta_testing_endpoint_returns_404_when_disabled(self):
        response = self.client.get('/beta_external_testing/')
        self.assertEqual(response.status_code, 404)

    @override_settings(FLAGS={'BETA_EXTERNAL_TESTING': [('boolean', True)]})
    def test_beta_testing_endpoint_returns_200_when_enabled(self):
        response = self.client.get('/beta_external_testing/')
        self.assertEqual(response.status_code, 200)
