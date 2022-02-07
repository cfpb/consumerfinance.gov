import json

from django.test import TestCase

from wagtail.core import blocks
from wagtail.tests.utils import WagtailTestUtils

from v1.atomic_elements.organisms import (
    ContactExpandable, ContactExpandableGroup
)
from v1.models import Contact


class ContactExpandableTests(TestCase):
    def test_render(self):
        contact = Contact.objects.create(
            heading="Scrooge McDuck",
            body="World's richest duck",
            contact_info=json.dumps([
                {
                    'type': 'hyperlink',
                    'value': {
                        'url': 'https://vault.duckburg.com',
                        'text': 'Money Bin',
                    },
                },
            ])
        )

        block = ContactExpandable()
        html = block.render(block.to_python({'contact': contact.pk}))

        self.assertIn("Scrooge McDuck", html)
        self.assertNotIn("World's richest duck", html, msg=(
            "ContactExpandable molecule should not include the Contact body"
        ))
        self.assertInHTML(
            '<a href="https://vault.duckburg.com">Money Bin</a>',
            html
        )

    def test_bulk_to_python(self):
        Contact.objects.bulk_create(
            Contact(pk=i, heading=str(i))
            for i in range(3)
        )

        class TestStreamBlock(blocks.StreamBlock):
            contact = ContactExpandable()

        block = TestStreamBlock()
        value = blocks.StreamValue(
            block,
            [
                {'type': 'contact', 'value': {'contact': 0}},
                {'type': 'contact', 'value': {'contact': 1}},
                {'type': 'contact', 'value': {'contact': 2}},
            ],
            is_lazy=True
        )

        # This verifies that the block does a single database query to retrieve
        # all 3 Contacts, even though they are split up between three different
        # ContactExpandable blocks.
        with self.assertNumQueries(1):
            block.render(value)


class ContactExpandableGroupTests(WagtailTestUtils, TestCase):
    def setUp(self):
        Contact.objects.bulk_create(
            Contact(
                pk=i,
                heading=str(i),
                contact_info=json.dumps([
                    {
                        'type': 'hyperlink',
                        'value': {
                            'url': 'https://%d.example.com' % i,
                        },
                    },
                ])
            ) for i in range(10)
        )

    def test_render(self):
        block = ContactExpandableGroup()
        html = block.render(block.to_python({
            'heading': "Contacts",
            'expandables': [
                {'contact': pk}
                for pk in (5, 3, 2, 1, 8)
            ],
        }))

        self.assertInHTML("<h3>Contacts</h3>", html)
        self.assertInHTML(
            '<a href="https://8.example.com">https://8.example.com</a>',
            html
        )

    def test_bulk_to_python(self):
        class TestStreamBlock(blocks.StreamBlock):
            contacts = ContactExpandableGroup()

        block = TestStreamBlock()
        value = blocks.StreamValue(
            block,
            [
                {
                    'type': 'contacts',
                    'value': {
                        'heading': 'First',
                        'expandables': [
                            {'contact': pk}
                            for pk in reversed(range(5))
                        ],
                    },
                },
                {
                    'type': 'contacts',
                    'value': {
                        'heading': 'Second',
                        'expandables': [
                            {'contact': pk}
                            for pk in reversed(range(5, 10))
                        ],
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
