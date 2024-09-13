from unittest import mock

from django.test import TestCase, override_settings

from wagtail.models import Site

from cdntools.backends import MOCK_PURGED
from teachers_digital_platform.models import ActivityPage, ActivitySetUp
from v1.models import (
    BlogPage,
    CFGOVPageCategory,
    LearnPage,
    NewsroomLandingPage,
    NewsroomPage,
    SublandingFilterablePage,
)
from v1.signals import invalidate_filterable_list_caches


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "cdntools.backends.MockCacheBackend",
        },
    }
)
class FilterableListInvalidationTestCase(TestCase):
    def setUp(self):
        self.root_page = Site.objects.first().root_page

        self.filterable_list_page = SublandingFilterablePage(title="Blog")
        self.root_page.add_child(instance=self.filterable_list_page)
        self.filterable_list_page.save()

        self.category_filterable_list_page = NewsroomLandingPage(title="News")
        self.root_page.add_child(instance=self.category_filterable_list_page)
        self.category_filterable_list_page.save()
        self.newsroom_page = NewsroomPage(title="News event")
        self.category_filterable_list_page.add_child(
            instance=self.newsroom_page
        )
        self.newsroom_page.save()

        self.blog_page = BlogPage(title="test blog")
        self.filterable_list_page.add_child(instance=self.blog_page)
        self.blog_page.categories.add(CFGOVPageCategory(name="op-ed"))
        self.blog_page.save()

        self.non_filterable_page = LearnPage(title="Page")
        self.root_page.add_child(instance=self.non_filterable_page)
        self.non_filterable_page.save()

        # Reset cache purged URLs after each test
        MOCK_PURGED[:] = []

    @mock.patch("v1.signals.cache")
    def test_invalidate_filterable_list_caches(
        self,
        mock_cache,
    ):
        invalidate_filterable_list_caches(None, instance=self.blog_page)

        for cache_key_prefix in (
            self.filterable_list_page.get_cache_key_prefix(),
            self.category_filterable_list_page.get_cache_key_prefix(),
        ):
            mock_cache.delete.assert_any_call(
                f"{cache_key_prefix}-all_filterable_results"
            )
            mock_cache.delete.assert_any_call(f"{cache_key_prefix}-page_ids")
            mock_cache.delete.assert_any_call(f"{cache_key_prefix}-topics")

        self.assertIn(self.filterable_list_page.slug, MOCK_PURGED)

    @mock.patch("django.core.cache.cache")
    def test_invalidate_filterable_list_caches_does_nothing(self, mock_cache):
        invalidate_filterable_list_caches(
            None, instance=self.non_filterable_page
        )
        mock_cache.delete.assert_not_called()
        self.assertEqual(MOCK_PURGED, [])


class RefreshActivitiesTestCase(TestCase):
    fixtures = ["tdp_minimal_data"]

    def setUp(self):
        self.root_page = Site.objects.first().root_page
        self.activity_page = ActivityPage(
            title="activity 1",
            live=False,
            summary="Summary",
            big_idea="Big Idea",
            essential_questions="Essential Questions",
            objectives="Objectives",
            what_students_will_do="What students will do",
            activity_duration_id=1,
            activity_file_id=8335,
        )
        self.root_page.add_child(instance=self.activity_page)
        self.activity_page.save()
        self.activity_page2 = ActivityPage(
            title="activity 2",
            live=False,
            summary="Summary 2",
            big_idea="Big Idea",
            essential_questions="Essential Questions",
            objectives="Objectives",
            what_students_will_do="What students will do",
            activity_duration_id=1,
            activity_file_id=8335,
        )
        self.root_page.add_child(instance=self.activity_page2)
        self.activity_page2.save()

    def test_setup_object_missing(self):
        self.assertFalse(ActivitySetUp.objects.exists())

    def test_publishing_creates_setup_object_with_reference(self):
        self.activity_page.save_revision().publish()
        self.assertTrue(ActivitySetUp.objects.exists())
        self.assertIn(
            str(self.activity_page.pk),
            ActivitySetUp.objects.first().card_setup,
        )
        self.assertEqual(len(ActivitySetUp.objects.first().card_setup), 1)

    def test_publish(self):
        self.activity_page.save_revision().publish()
        self.activity_page2.save_revision().publish()
        self.assertEqual(len(ActivitySetUp.objects.first().card_setup), 2)
        for page in [self.activity_page, self.activity_page2]:
            self.assertIn(
                str(page.pk), ActivitySetUp.objects.first().card_setup
            )

    def test_upublish(self):
        self.activity_page.save_revision().publish()
        self.activity_page2.save_revision().publish()
        self.activity_page2.refresh_from_db()
        self.assertTrue(self.activity_page2.live)
        self.activity_page2.unpublish()
        self.activity_page2.refresh_from_db()
        self.assertFalse(self.activity_page2.live)
        setup = ActivitySetUp.objects.first()
        self.assertNotIn(str(self.activity_page2.pk), setup.card_setup)
        self.assertEqual(len(ActivitySetUp.objects.first().card_setup), 1)
