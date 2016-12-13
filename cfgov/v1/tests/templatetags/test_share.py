import mock

from django.template import Context, Template
from unittest import TestCase
from wagtail.wagtailcore.models import Site

from v1.templatetags import share
from v1.tests.wagtail_pages import helpers
from v1.models.base import (
    CFGOVPage, CFGOVPagePermissionTester, CFGOVUserPagePermissionsProxy, User
)


class TemplatetagsShareTestCase(TestCase):

    def setUp(self):
        """
        Create a new page, a User, and a couple of mock objects that
        simulate the context and request. There are also a couple of
        side effect functions for accessing the mocks as dictionaries.
        Also an object that is not a page and doesn't do anything, but
        has a `.specific` member variable.
        """

        self.page = CFGOVPage(title='a very nice cfgov page')
        self.page.shared = False
        self.page.live = False
        self.not_a_page = mock.MagicMock()
        self.not_a_page.specific = mock.MagicMock()

        helpers.save_new_page(self.page)

        self.user = User(first_name='A', last_name='User')
        self.user.save()

        self.context = mock.MagicMock()
        self.request = mock.MagicMock()

        self.context_dict = {}

        def context_getitem(name):
            return self.context_dict[name]

        def context_setitem(name, value):
            self.context_dict[name] = value

        self.context.__getitem__.side_effect = context_getitem
        self.context.__setitem__.side_effect = context_setitem

        self.request.user = self.user
        self.site_objects = Site.objects.all()

    def tearDown(self):

        self.user.delete()

    def test_is_shared(self):
        """
        Test if the `is_shared` function properly reports a page as shared.
        Something that is not an instance of the Page class should return None
        while otherwise the `.shared` property controls whether a page is
        shared or not.
        """

        result = share.is_shared(self.not_a_page)

        self.assertIsNone(result)

        self.page.shared = True
        self.page.save()
        result = share.is_shared(self.page)

        self.assertTrue(result)

        self.page.shared = False
        self.page.save()
        result = share.is_shared(self.page)

        self.assertFalse(result)

    def test_get_page_state_url_non_live_non_shared(self):
        """
        If a page is neither live nor shared, the url returned
        should be None.
        """

        self.page.live = False
        self.page.shared = False
        self.page.save()

        result = share.get_page_state_url(None, self.page)
        self.assertIsNone(result)

    def test_get_page_state_url_staged(self):
        """
        If the page is shared and staged, return the url with the hostname
        replaced by the hostname of the staging server. Here we check against
        the replaced version of the page.url because the final url of the
        saved page can vary depending on the order in which objects are saved,
        so there's no hard-coded "ground truth" to compare to.
        """
        self.page.live = False
        self.page.shared = True
        self.page.save()

        result = share.get_page_state_url(None, self.page)
        self.assertEqual(result, self.page.url.replace('http://localhost',
                                                       'http://content.localhost'))

    def test_get_page_state_url_live(self):
        """
        If the page is live and shared, and attached to the host root, but not
        staged, then the result url should be just the same as the page.url.
        """
        self.page.live = True
        self.page.shared = False
        self.page.save()

        result = share.get_page_state_url(None, self.page)
        self.assertEqual(result, self.page.url)

    def test_v1page_permissions_no_permissions_in_context(self):
        """
        If the key 'user_page_permissions' is not present in the context dictionary,
        use the CFGOVUserPagePermissionsProxy object for the user to retrieve the
        CFGOVPagePermissionTester object. This test just checks that such an object
        is returned.
        """
        self.context_dict = {'request': self.request}

        result = share.v1page_permissions(self.context, self.page)

        self.assertIsInstance(result, CFGOVPagePermissionTester)

    def test_v1page_permissions_permissions_in_context(self):
        """
        Like the above test, but this time 'user_page_permissions' is present, and
        is set by CFGOVUserPagePermissionsProxy for the user ahead of time. Checks
        to see if the CFGOVPagePermissionTester is returned.
        """

        self.context_dict = {'request': self.request,
                             'user_page_permissions': CFGOVUserPagePermissionsProxy(self.user)}

        result = share.v1page_permissions(self.context, self.page)

        self.assertIsInstance(result, CFGOVPagePermissionTester)

    def test_get_page_state_url_no_url(self):
        """
        If a page is live and/or shared, but is not connected to a site root,
        return None. In order for this to work, we temporarily delete all Site
        objects but then we just restore them again.
        """

        self.page.shared = True
        self.page.live = True
        self.page.save()

        site_objects = Site.objects.all()
        for site in site_objects:
            site.delete()

        result = share.get_page_state_url(None, self.page)

        for site in site_objects:
            site.save()

        self.assertIsNone(result)


class TemplateRenderingTest(TestCase):
    def test_template_renders_with_get_page_state_url(self):
        site = Site.objects.get(is_default_site=True)
        page = site.root_page

        template = (
            '{% load share %}'
            '{% get_page_state_url page as url %}'
            '{{ url }}'
        )

        t = Template(template)
        c = Context({'page': page})
        self.assertEquals(t.render(c), page.url)
