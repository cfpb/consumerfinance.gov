import json

from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase

from wagtail.core.models import Page, Site
from wagtail.tests.testapp.models import DefaultStreamPage

from v1.query import StreamBlockPageQuerySet


class StreamBlockPageQuerySetTestCase(TestCase):
    def setUp(self):
        root_page = Site.objects.get(is_default_site=True).root_page
        test_page = DefaultStreamPage(
            title="Test page",
            live=True,
            body=json.dumps(
                [
                    {"type": "text", "value": "Test text"},
                ]
            ),
        )
        root_page.add_child(instance=test_page)
        other_page = DefaultStreamPage(
            title="Other page",
            live=True,
            body=json.dumps(
                [
                    {"type": "rich_text", "value": "rich text"},
                    {"type": "rich_text", "value": "another rich text"},
                ]
            ),
        )
        root_page.add_child(instance=other_page)

    def test_block_in_field(self):
        """Ensure that block_in_field finds an appropriate number of expected
        results."""
        queryset = StreamBlockPageQuerySet(DefaultStreamPage)
        self.assertEqual(queryset.count(), 2)

        text_queryset = queryset.block_in_field("text", "body")
        self.assertEqual(text_queryset.count(), 1)

        image_queryset = queryset.block_in_field("image", "body")
        self.assertEqual(image_queryset.count(), 0)

    def test_block_in_field_wrong_fields(self):
        """If the field doesn't exist or isn't a StreamField,
        block_in_field should raise FieldDoesNotExist or TypeError
        respectively."""
        queryset = StreamBlockPageQuerySet(Page)

        # If we ask for a block in a field the model doesn't have, it should
        # raise a FieldDoesNotExist
        with self.assertRaises(FieldDoesNotExist):
            queryset.block_in_field("text", "field_that_doesnt_exist")

        # If we ask for a block in a field that isn't a StreamField, it should
        # raise a TypeError
        with self.assertRaises(TypeError):
            queryset.block_in_field("text", "title")

    def test_annotate_block_in(self):
        """Ensure we get an annotation for a target block"""
        queryset = StreamBlockPageQuerySet(DefaultStreamPage)

        annotated_queryset = queryset.block_in_field(
            "text", "body"
        ).annotate_block_in("text", "body")
        self.assertEqual(annotated_queryset.count(), 1)
        self.assertEqual(annotated_queryset[0].text_value, "Test text")

    def test_annotate_block_in_multiple_blocks(self):
        """If we have multiple target_blocks in a StreamField, ensure we only
        get an annotation for the first one."""
        queryset = StreamBlockPageQuerySet(DefaultStreamPage)

        annotated_queryset = queryset.block_in_field(
            "rich_text", "body"
        ).annotate_block_in("rich_text", "body")
        self.assertEqual(annotated_queryset.count(), 1)
        self.assertEqual(annotated_queryset[0].rich_text_value, "rich text")

    def test_annotate_block_in_when_block_doesnt_exist(self):
        """If asked to annotate with a block that doesn't exist in the
        streamfield in the queryset, the annotation should be None"""
        queryset = StreamBlockPageQuerySet(DefaultStreamPage)

        annotated_queryset = queryset.annotate_block_in("foo", "body")
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
            queryset.annotate_block_in("text", "field_that_doesnt_exist")

        # If we ask for a block in a field that isn't a StreamField, it should
        # raise a TypeError
        with self.assertRaises(TypeError):
            queryset.annotate_block_in("text", "title")
