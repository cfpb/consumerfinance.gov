from django.http import HttpRequest
from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore import blocks

from v1.atomic_elements.organisms import ContactExpandableGroup
from v1.models import Contact


class TestContactExpandableGroup(WagtailTestUtils, TestCase):
    def test_renders_with_heading_id(self):
        Contact.objects.create(pk=1, heading='Bill S. Preston, Esq.')
        Contact.objects.create(pk=2, heading='"Ted" Theodore Logan')

        block = ContactExpandableGroup()
        value = block.to_python({
            'group_title': 'Wyld Stallyns',
            'contacts': [1, 2],
        })
        html = block.render(value)
        self.assertTagInHTML(html, '<div id="wyld-stallyns">')
        self.assertIn('Bill', html)
        self.assertIn('Ted', html)

    def test_renders_unique_heading_ids(self):
        block = ContactExpandableGroup()
        value = block.to_python({
            'group_title': 'Heading',
            'contacts': [],
        })

        request = HttpRequest()
        html = block.render(value, {'request': request})
        self.assertTagInHTML(html, '<div id="heading">')

        html = block.render(value, {'request': request})
        self.assertTagInHTML(html, '<div id="heading-1">')

    def test_bulk_to_python(self):
        Contact.objects.bulk_create(
            Contact(pk=i, heading=str(i)) for i in range(10)
        )

        class TestStreamBlock(blocks.StreamBlock):
            contacts = ContactExpandableGroup()

        block = TestStreamBlock()
        value = blocks.StreamValue(
            block,
            [
                {
                    'type': 'contacts',
                    'value': {
                        'group_title': 'First',
                        'contacts': list(range(5)),
                    },
                },
                {
                    'type': 'contacts',
                    'value': {
                        'group_title': 'Second',
                        'contacts': list(range(5, 10))
                    },
                },
            ],
            is_lazy=True
        )

        # This verifies that the block does a single database query to retrieve
        # all 10 Contacts, even though they are split up between two different
        # ContactExpandableGroup blocks.
        with self.assertNumQueries(1):
            block.render(value)
