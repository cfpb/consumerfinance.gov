from unittest import TestCase, mock

from django.contrib.auth.models import User
from django.utils import timezone

from wagtail.core.models import Site

from model_bakery import baker

from v1.models import (
    BlogPage, CFGOVPage, CFGOVPageCategory, NewsroomLandingPage,
    SublandingFilterablePage
)
from v1.signals import invalidate_filterable_list_caches
from v1.tests.wagtail_pages.helpers import publish_page, save_new_page


class UserSaveTestCase(TestCase):
    def make_user(self, password, is_superuser=False):
        user = baker.prepare(User, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def test_user_save_new_password_makes_history_item(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()

        user.set_password('bar')
        user.save()
        new_phi = user.passwordhistoryitem_set.latest()

        self.assertNotEqual(first_phi, new_phi)
        self.assertEqual(user.password, new_phi.encrypted_password)

    def test_user_save_new_password_not_expired(self):
        user = self.make_user(password='foo')
        user.set_password('bar')
        user.save()

        new_phi = user.passwordhistoryitem_set.latest()
        self.assertGreater(new_phi.expires_at, timezone.now())

    def test_user_save_new_password_locks_password(self):
        user = self.make_user(password='foo')
        user.set_password('bar')
        user.save()

        new_phi = user.passwordhistoryitem_set.latest()
        self.assertGreater(new_phi.locked_until, timezone.now())

    def test_user_save_same_password_no_history_item(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()

        user.save()
        new_phi = user.passwordhistoryitem_set.latest()

        self.assertEqual(first_phi, new_phi)
        self.assertEqual(user.password, new_phi.encrypted_password)

    def test_user_created_expires_password(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertLess(first_phi.expires_at, timezone.now())

    def test_user_created_unlocks_password(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertLess(first_phi.locked_until, timezone.now())

    def test_superuser_created_does_not_expire_password(self):
        user = self.make_user(password='foo', is_superuser=True)
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertGreater(first_phi.expires_at, timezone.now())

    def test_superuser_created_unlocks_password(self):
        user = self.make_user(password='foo', is_superuser=True)
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertLess(first_phi.locked_until, timezone.now())


class FilterableListInvalidationTestCase(TestCase):

    def setUp(self):
        self.root_page = Site.objects.first().root_page

        self.filterable_list_page = SublandingFilterablePage(
            title='Blog'
        )
        self.root_page.add_child(instance=self.filterable_list_page)
        self.filterable_list_page.save()

        self.category_filterable_list_page = NewsroomLandingPage(
            title="News"
        )
        self.root_page.add_child(instance=self.category_filterable_list_page)
        self.category_filterable_list_page.save()

        self.blog_page = BlogPage(title='test blog')
        self.filterable_list_page.add_child(instance=self.blog_page)
        self.blog_page.categories.add(CFGOVPageCategory(name='op-ed'))
        self.blog_page.save()

        self.non_filterable_page = CFGOVPage(title='Page')
        self.root_page.add_child(instance=self.non_filterable_page)
        self.non_filterable_page.save()

    @mock.patch('v1.signals.PurgeBatch')
    @mock.patch('v1.signals.cache')
    def test_invalidate_filterable_list_caches(
        self, mock_cache, mock_purge_batch,
    ):
        invalidate_filterable_list_caches(None, instance=self.blog_page)

        for cache_key_prefix in (
            self.filterable_list_page.get_cache_key_prefix(),
            self.category_filterable_list_page.get_cache_key_prefix()
        ):
            mock_cache.delete.assert_any_call(
                f"{cache_key_prefix}-all_filterable_results"
            )
            mock_cache.delete.assert_any_call(
                f"{cache_key_prefix}-page_ids"
            )
            mock_cache.delete.assert_any_call(
                f"{cache_key_prefix}-topics"
            )
            mock_cache.delete.assert_any_call(
                f"{cache_key_prefix}-authors"
            )

        mock_purge_batch().add_page.assert_any_call(self.filterable_list_page)

    @mock.patch('django.core.cache.cache')
    def test_invalidate_filterable_list_caches_does_nothing(self, mock_cache):
        invalidate_filterable_list_caches(
            None,
            instance=self.non_filterable_page
        )
        mock_cache.delete.assert_not_called()
