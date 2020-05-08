import json

from django.test import RequestFactory, TestCase
from django.utils.text import slugify

from wagtail.core.models import Page, Site

from mega_menu.frontend_conversion import FrontendConverter
from mega_menu.models import Menu


class FrontendConverterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = Site.objects.get(is_default_site=True).root_page

        consumer_tools_page = cls.make_test_page('Consumer Tools')
        about_us_page = cls.make_test_page('About Us')
        auto_loans_page = cls.make_test_page('Auto Loans')
        bank_accounts_page = cls.make_test_page('Bank Accounts')
        well_being_page = cls.make_test_page('Financial Well-Being')

        submenus = [
            {
                'type': 'submenu',
                'value': {
                    'overview_page': consumer_tools_page.pk,
                    'columns': [
                        {
                            'heading': 'Money Topics',
                            'links': [
                                {
                                    'page': auto_loans_page.pk,
                                },
                                {
                                    'page': bank_accounts_page.pk,
                                    'text': 'Wagtail page with other text',
                                },
                                {
                                    'url': '/foo/bar/',
                                    'text': 'Non-Wagtail page',
                                },
                            ],
                        },
                    ],
                    'featured_links': [
                        {
                            'url': '/featured/1/',
                            'text': 'First featured link',
                        },
                    ],
                },
            },
            {
                'type': 'submenu',
                'value': {
                    'overview_page': about_us_page.pk,
                    'title': 'Alternate Submenu Title',
                    'featured_links': [
                        {
                            'url': '/featured/2/',
                            'text': 'Second featured link',
                        },
                        {
                            'url': '/featured/3/',
                            'text': 'Third featured link',
                        },
                    ],
                    'other_links': [
                        {
                            'page': well_being_page.pk,
                            'text': 'First other link',
                            'icon': 'star',
                        },
                        {
                            'url': '/other/2/',
                            'text': 'Second other link',
                            'icon': 'mail',
                        },
                    ]
                },
            },
        ]

        cls.menu = Menu.objects.create(
            language='en',
            submenus=json.dumps(submenus)
        )

    @classmethod
    def make_test_page(cls, title):
        page = Page(title=title, slug=slugify(title))
        cls.root_page.add_child(instance=page)
        return page

    def do_conversion(self, menu):
        request = RequestFactory().get('/consumer-tools/')
        converter = FrontendConverter(menu, request=request)
        return converter.get_menu_items()

    def test_converted_format_uses_basic_python_types(self):
        converted = self.do_conversion(self.menu)

        # We want to pass only basic Python types (strings, etc.) to the
        # frontend, as opposed to complex Wagtail types like Pages. An easy
        # way to test this is to test JSON serialization.
        self.assertEqual(converted, json.loads(json.dumps(converted)))

    def test_conversion_database_queries(self):
        self.menu.refresh_from_db()

        # We expect to see two queries here:
        #
        # 1. Wagtail's site root lookup.
        # 2. Single query to retrieve all pages at once.
        with self.assertNumQueries(2):
            self.do_conversion(self.menu)

    def test_conversion_output(self):
        self.assertEqual(self.do_conversion(self.menu), [
            {
                'selected': True,
                'overview': {
                    'url': '/consumer-tools/',
                    'text': 'Consumer Tools',
                    'selected': True,
                },
                'nav_groups': [
                    {
                        'title': 'Money Topics',
                        'title_hidden': False,
                        'nav_items': [
                            {
                                'url': '/auto-loans/',
                                'text': 'Auto Loans',
                            },
                            {
                                'url': '/bank-accounts/',
                                'text': 'Wagtail page with other text',
                            },
                            {
                                'url': '/foo/bar/',
                                'text': 'Non-Wagtail page',
                            },
                        ],
                    },
                ],
                'featured_items': [
                    {
                        'url': '/featured/1/',
                        'text': 'First featured link',
                    },
                ],
            },
            {
                'overview': {
                    'url': '/about-us/',
                    'text': 'Alternate Submenu Title',
                },
                'featured_items': [
                    {
                        'url': '/featured/2/',
                        'text': 'Second featured link',
                    },
                    {
                        'url': '/featured/3/',
                        'text': 'Third featured link',
                    },
                ],
                'other_items': [
                    {
                        'url': '/financial-well-being/',
                        'text': 'First other link',
                        'icon': 'star',
                    },
                    {
                        'url': '/other/2/',
                        'text': 'Second other link',
                        'icon': 'mail',
                    },
                ],
            },
        ])
