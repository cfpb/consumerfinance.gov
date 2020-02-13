import json

from django.test import RequestFactory, TestCase
from django.utils.text import slugify

from wagtail.wagtailcore.models import Page, Site
from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.tests.utils import get_test_image_file

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

        cls.test_image_1, cls.test_rendition_1 = cls.make_test_image()
        cls.test_image_2, cls.test_rendition_2 = cls.make_test_image()

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
                                    'link': {
                                        'page': auto_loans_page.pk,
                                    },
                                    'children': [
                                        {
                                            'url': '/foo/bar/',
                                            'text': 'Non-Wagtail page',
                                        },
                                    ],
                                },
                                {
                                    'link': {
                                        'page': bank_accounts_page.pk,
                                        'text': 'Wagtail page with other text',
                                    },
                                },
                                {
                                    'link': {
                                        'url': '/foo/baz/',
                                        'text': 'Another non-Wagtail page',
                                    },
                                },
                            ],
                        },
                    ],
                    'featured_links': [
                        {
                            'link': {
                                'url': '/featured/1/',
                                'text': 'First featured link',
                            },
                            'body': 'First featured body',
                            'image': cls.test_image_1.pk,
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
                            'link': {
                                'url': '/featured/2/',
                                'text': 'Second featured link',
                            },
                            'body': 'Second featured body',
                            'image': cls.test_image_2.pk,
                        },
                        {
                            'link': {
                                'url': '/featured/3/',
                                'text': 'Third featured link',
                            },
                        },
                    ],
                    'other_links': [
                        {
                            'link': {
                                'page': well_being_page.pk,
                                'text': 'First other link',
                            },
                            'icon': 'star',
                        },
                        {
                            'link': {
                                'url': '/other/2/',
                                'text': 'Second other link',
                            },
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

    @classmethod
    def make_test_image(cls):
        image = get_image_model().objects.create(
            title='test',
            file=get_test_image_file()
        )
        return image, image.get_rendition('original')

    def do_conversion(self, menu):
        request = RequestFactory().get('/')
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

        # We expect to see five queries here:
        #
        # 1. Wagtail's site root lookup.
        # 2. Single query to retrieve all pages at once.
        # 3. Single query to retrieve all featured images at once.
        # 4,5. One query each to retrieve a rendition for the first image in
        # the featured menu content for each column.
        with self.assertNumQueries(5):
            self.do_conversion(self.menu)

    def test_conversion_output(self):
        self.assertEqual(self.do_conversion(self.menu), [
            {
                'link': {
                    'external_link': '/consumer-tools/',
                    'link_text': 'Consumer Tools',
                },
                'nav_groups': [
                    {
                        'value': {
                            'group_title': 'Money Topics',
                            'hide_group_title': False,
                            'nav_items': [
                                {
                                    'external_link': '/auto-loans/',
                                    'link_text': 'Auto Loans',
                                    'nav_items': [
                                        {
                                            'external_link': '/foo/bar/',
                                            'link_text': 'Non-Wagtail page',
                                        },
                                    ],
                                },
                                {
                                    'external_link': '/bank-accounts/',
                                    'link_text': (
                                        'Wagtail page with other text'
                                    ),
                                },
                                {
                                    'external_link': '/foo/baz/',
                                    'link_text': 'Another non-Wagtail page',
                                },
                            ]
                        },
                    },
                ],
                'featured_content': {
                    'value': {
                        'link': {
                            'external_link': '/featured/1/',
                            'link_text': 'First featured link',
                        },
                        'body': 'First featured body',
                        'image': {
                            'url': self.test_rendition_1.url,
                        },
                    },
                },
                'featured_links': [
                    {
                        'external_link': '/featured/1/',
                        'link_text': 'First featured link',
                    },
                ],
            },
            {
                'link': {
                    'external_link': '/about-us/',
                    'link_text': 'Alternate Submenu Title',
                },
                'featured_content': {
                    'value': {
                        'link': {
                            'external_link': '/featured/2/',
                            'link_text': 'Second featured link',
                        },
                        'body': 'Second featured body',
                        'image': {
                            'url': self.test_rendition_2.url,
                        },
                    },
                },
                'featured_links': [
                    {
                        'external_link': '/featured/2/',
                        'link_text': 'Second featured link',
                    },
                    {
                        'external_link': '/featured/3/',
                        'link_text': 'Third featured link',
                    },
                ],
                'footer': (
                    '<p>'
                    '<span aria-hidden="true">First other link</span> '
                    '<a aria-label="First other link Financial Well-Being" '
                    'href="/financial-well-being/">Financial Well-Being</a>'
                    '</p>\n'
                    '<p>'
                    '<a href="/other/2/">Second other link</a>'
                    '</p>'
                ),
                'other_links': [
                    {
                        'external_link': '/financial-well-being/',
                        'link_text': 'First other link',
                        'icon': 'star',
                    },
                    {
                        'external_link': '/other/2/',
                        'link_text': 'Second other link',
                        'icon': 'mail',
                    },
                ],
            },
        ])
