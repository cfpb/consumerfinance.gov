from django.test import TestCase
from wagtail.wagtailcore.models import Page

from scripts.create_careers_pages import create_careers_pages
from v1.tests.wagtail_pages.helpers import save_page


class TestCreateCareersPages(TestCase):
    def setUp(self):
        self.slugs = (
            'about-us',
            'careers',
            'working-at-cfpb',
            'application-process',
            'students-and-graduates',
            'current-openings',
        )

    def test_assert_careers_pages_do_not_exist_before_script(self):
        for slug in self.slugs:
            with self.assertRaises(Page.DoesNotExist):
                Page.objects.get(slug=slug)

    def test_assert_careers_pages_created_by_script(self):
        create_careers_pages()
        for slug in self.slugs:
            self.assertTrue(Page.objects.filter(slug=slug).exists())

    def test_assert_script_can_run_multiple_times(self):
        create_careers_pages()
        create_careers_pages()

    def test_assert_script_keeps_page_content_if_pages_already_exist(self):
        create_careers_pages()

        careers = Page.objects.get(slug='careers')
        careers.title = 'test title'
        save_page(careers)

        create_careers_pages()

        careers_after_rerun = Page.objects.get(slug='careers')
        self.assertEqual(careers_after_rerun.title, 'test title')
