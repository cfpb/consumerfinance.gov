from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from v1.atomic_elements.organisms import ContactExpandableGroup
from v1.models import Contact


class TestContactExpandableGroup(WagtailTestUtils, TestCase):
    def test_renders_with_heading_id(self):
        Contact.objects.create(heading='Bill S. Preston, Esq.')
        Contact.objects.create(heading='"Ted" Theodore Logan')

        block = ContactExpandableGroup()
        value = block.to_python({
            'group_title': 'Wyld Stallyns',
            'contacts': Contact.objects.values_list('pk', flat=True),
        })
        html = block.render(value)
        self.assertTagInHTML(html, '<div id="wyld-stallyns">')
        self.assertIn('Bill', html)
        self.assertIn('Ted', html)
