import json

from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase

from wagtail.models import Page, Site

from v1.models import SublandingPage
from v1.query import StreamBlockPageQuerySet


class StreamBlockPageQuerySetTestCase(TestCase):
    def setUp(self):
        root_page = Site.objects.get(is_default_site=True).root_page
        test_page = SublandingPage(
            title="Test page",
            live=True,
            sidebar_breakout=json.dumps(
                [
                    {"type": "slug", "value": "Test slug"},
                ]
            ),
        )
        root_page.add_child(instance=test_page)
        other_page = SublandingPage(
            title="Other page",
            live=True,
            sidebar_breakout=json.dumps(
                [
                    {"type": "paragraph", "value": "rich text"},
                    {"type": "paragraph", "value": "another rich text"},
                ]
            ),
        )
        root_page.add_child(instance=other_page)

    def test_block_in_field(self):
        """Ensure that block_in_field finds an appropriate number of expected
        results."""
        queryset = StreamBlockPageQuerySet(SublandingPage)
        self.assertEqual(queryset.count(), 2)

        heading_queryset = queryset.block_in_field("slug", "sidebar_breakout")
        self.assertEqual(heading_queryset.count(), 1)

        image_queryset = queryset.block_in_field("image", "sidebar_breakout")
        self.assertEqual(image_queryset.count(), 0)

    def test_block_in_field_wrong_fields(self):
        """If the field doesn't exist or isn't a StreamField,
        block_in_field should raise FieldDoesNotExist or TypeError
        respectively."""
        queryset = StreamBlockPageQuerySet(Page)

        # If we ask for a block in a field the model doesn't have, it should
        # raise a FieldDoesNotExist
        with self.assertRaises(FieldDoesNotExist):
            queryset.block_in_field("heading", "field_that_doesnt_exist")

        # If we ask for a block in a field that isn't a StreamField, it should
        # raise a TypeError
        with self.assertRaises(TypeError):
            queryset.block_in_field("heading", "title")

    def test_annotate_block_in(self):
        """Ensure we get an annotation for a target block"""
        queryset = StreamBlockPageQuerySet(SublandingPage)

        annotated_queryset = queryset.block_in_field(
            "slug", "sidebar_breakout"
        ).annotate_block_in("slug", "sidebar_breakout")
        self.assertEqual(annotated_queryset.count(), 1)
        self.assertEqual(annotated_queryset[0].slug_value, "Test slug")

    def test_annotate_block_in_multiple_blocks(self):
        """If we have multiple target_blocks in a StreamField, ensure we only
        get an annotation for the first one."""
        queryset = StreamBlockPageQuerySet(SublandingPage)

        annotated_queryset = queryset.block_in_field(
            "paragraph", "sidebar_breakout"
        ).annotate_block_in("paragraph", "sidebar_breakout")
        self.assertEqual(annotated_queryset.count(), 1)
        self.assertEqual(annotated_queryset[0].paragraph_value, "rich text")

    def test_annotate_block_in_when_block_doesnt_exist(self):
        """If asked to annotate with a block that doesn't exist in the
        streamfield in the queryset, the annotation should be None"""
        queryset = StreamBlockPageQuerySet(SublandingPage)

        annotated_queryset = queryset.annotate_block_in(
            "foo", "sidebar_breakout"
        )
        self.assertTrue(annotated_queryset.count() > 0)
        self.assertEqual(annotated_queryset[0].foo_value, None)

    def test_annotate_block_in_wrong_fields(self):
        """If the field doesn't exist or isn't a StreamField,
        annotate_block_in should raise FieldDoesNotExist or TypeError
        respectively."""
        queryset = StreamBlockPageQuerySet(Page)

        # If we ask for a block in a field the model doesn't have, it should
        # raise a FieldDoesNotExist
        with self.assertRaises(FieldDoesNotExist):
            queryset.annotate_block_in("heading", "field_that_doesnt_exist")

        # If we ask for a block in a field that isn't a StreamField, it should
        # raise a TypeError
        with self.assertRaises(TypeError):
            queryset.annotate_block_in("heading", "title")
