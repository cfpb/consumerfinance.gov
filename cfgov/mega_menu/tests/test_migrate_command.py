# -*- coding: utf-8 -*-
import json

from django.core.management import call_command
from django.test import TestCase
from django.utils.text import slugify

try:
    from wagtail.core.models import Page, Site
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.models import Page, Site

from mega_menu.models import Menu
from v1.models import MenuItem


class MigrateMenuContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        about_us_page = cls.make_test_page('About us')

        es_root = cls.make_test_page('es')
        cls.make_test_page('Herramientas del consumidor', root_page=es_root)
        cls.make_test_page('Obtener respuestas', root_page=es_root)
        cls.make_test_page('Enviar una queja', root_page=es_root)
        cls.make_test_page('Quiénes somos', root_page=es_root)

        MenuItem.objects.create(
            link_text='English menu',
            column_4=json.dumps([
                {
                    'type': 'nav_group',
                    'value': {
                        'group_title': 'Heading',
                        'hide_group_title': None,
                        'nav_items': [],
                    },
                },
                {
                    'type': 'featured_content',
                    'value': {
                        'link': {
                            'link_text': 'Link text',
                            'external_link': '/somewhere/',
                        },
                    },
                },
            ]),
            nav_footer=json.dumps([
                {
                    'type': 'nav_footer',
                    'value': {
                        'content': '<p><a href="/foo/">bar</a></p>',
                    }
                },
                {
                    'type': 'nav_footer',
                    'value': {
                        'content': (
                            '<p>Link: <a linktype="page" id="{}">page</a></p>'
                        ).format(about_us_page.pk),
                    }
                },
            ])
        )

    @classmethod
    def make_test_page(cls, title, root_page=None):
        if not root_page:
            root_page = Site.objects.get(is_default_site=True).root_page

        page = Page(title=title, slug=slugify(title))
        root_page.add_child(instance=page)
        return page

    def test_command(self):
        call_command('migrate_menu_content')

        english = Menu.objects.get(language='en')
        self.assertEqual(len(english.submenus.stream_data), 1)

        spanish = Menu.objects.get(language='es')
        self.assertEqual(len(spanish.submenus.stream_data), 4)
