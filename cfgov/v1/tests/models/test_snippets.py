from django.test import TestCase
from wagtail.wagtailcore.models import Site

from v1.models.snippets import (TaggableSnippetManager, Resource)


class TestFilterByTags(TestCase):
    def setUp(self):
        self.snippet1 = Resource.objects.create(title='Test snippet 1')
        self.snippet1.tags.add('tagA')
        self.snippet2 = Resource.objects.create(title='Test snippet 2')
        self.snippet2.tags.add('tagA')
        self.snippet2.tags.add('tagB')

    def test_empty_list_argument_returns_all(self):
        self.assertSequenceEqual(
            Resource.objects.filter_by_tags([]),
            [self.snippet1, self.snippet2]
        )

    def test_all_items_with_single_tag_are_returned(self):
        self.assertSequenceEqual(
            Resource.objects.filter_by_tags(['tagA']),
            [self.snippet1, self.snippet2]
        )

    def test_nothing_returned_when_tag_is_unused(self):
        self.assertSequenceEqual(
            Resource.objects.filter_by_tags(['tagC']),
            []
        )

    def test_item_with_multiple_tags_is_returned(self):
        self.assertIn(
            self.snippet2,
            Resource.objects.filter_by_tags(['tagA', 'tagB'])
        )

    def test_item_with_only_some_of_selected_tags_is_not_returned(self):
        self.assertNotIn(
            self.snippet1,
            Resource.objects.filter_by_tags(['tagA', 'tagB'])
        )
