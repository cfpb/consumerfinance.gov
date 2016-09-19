import mock

from unittest import TestCase
from v1.templatetags import share
from v1.tests.wagtail_pages import helpers
from v1.models.base import CFGOVPage, CFGOVPagePermissionTester, CFGOVUserPagePermissionsProxy, User


class TemplatetagsShareTestCase(TestCase):

    def setUp(self):

        self.page = CFGOVPage(title='a very nice cfgov page')
        self.shared = False
        self.live = False
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

    def tearDown(self):

        self.user.delete()

    def test_is_shared(self):

        result = share.is_shared(self.not_a_page)

        self.assertIsNone(result)

        self.page.shared = True
        result = share.is_shared(self.page)

        self.assertTrue(result)

        self.page.shared = False
        result = share.is_shared(self.page)

        self.assertFalse(result)

    def test_get_page_state_url_non_live_non_shared(self):

        self.page.live = False
        self.page.shared = False
        self.page.save()

        result = share.get_page_state_url(None, self.page)
        self.assertIsNone(result)

    def test_get_page_state_url_no_url(self):

        self.page.live = True
        self.page.url_path = ''
        self.page.shared = True
        self.page.save()

        result = share.get_page_state_url(None, self.page)
        self.assertIsNone(result)

    def test_get_page_state_url_staged(self):

        self.page.live = False
        self.page.shared = True
        self.page.save()

        result = share.get_page_state_url(None, self.page)
        self.assertEqual(result, 'http://content.localhost:8000/a-very-nice-cfgov-page-4/')

    def test_get_page_state_url_live(self):

        self.page.live = True
        self.page.shared = False
        self.page.save()

        result = share.get_page_state_url(None, self.page)
        self.assertEqual(result, self.page.url)

    def test_v1page_permissions_no_permissions_in_context(self):

        self.context_dict = {'request': self.request}

        result = share.v1page_permissions(self.context, self.page)

        self.assertIsInstance(result, CFGOVPagePermissionTester)

    def test_v1page_permissions_permissions_in_context(self):

        self.context_dict = {'request': self.request,
                             'user_page_permissions': CFGOVUserPagePermissionsProxy(self.user)}

        result = share.v1page_permissions(self.context, self.page)

        self.assertIsInstance(result, CFGOVPagePermissionTester)