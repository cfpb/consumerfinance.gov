from django.conf import settings
from django.test import SimpleTestCase, TestCase, override_settings

from wagtail.core.models import Page

from core.feature_flags import (
    environment_is, environment_is_not, in_split_testing_cluster
)
from v1.models import BrowsePage


class TestEnvironmentConditions(SimpleTestCase):
    @override_settings()
    def test_setting_not_defined(self):
        del settings.DEPLOY_ENVIRONMENT
        self.assertFalse(environment_is('foo'))
        self.assertTrue(environment_is_not('foo'))

    @override_settings(DEPLOY_ENVIRONMENT='foo')
    def test_setting_matches(self):
        self.assertTrue(environment_is('foo'))
        self.assertFalse(environment_is_not('foo'))

    @override_settings(DEPLOY_ENVIRONMENT='bar')
    def test_setting_does_not_match(self):
        self.assertFalse(environment_is('foo'))
        self.assertTrue(environment_is_not('foo'))


class TestSplitTestingCondition(TestCase):
    def setUp(self):
        TEST_CLUSTERS = {
            1: [4, 5, 6],
            2: [7, 8],
            3: [9],
        }
        self.CLUSTERS = {
            'TEST_CLUSTERS': TEST_CLUSTERS,
        }
        root_page = Page.objects.get(pk=1)
        self.page = BrowsePage(title="Split testing test page")
        root_page.add_child(instance=self.page)

    def test_basic_page_in_cluster(self):
        self.page.id = 9
        self.assertTrue(in_split_testing_cluster(
            'TEST_CLUSTERS',
            self.page,
            self.CLUSTERS,
        ))

    def test_basic_page_not_in_cluster(self):
        self.page.id = 1
        self.assertFalse(in_split_testing_cluster(
            'TEST_CLUSTERS',
            self.page,
            self.CLUSTERS,
        ))
