from django.test import RequestFactory, TestCase

from wagtail.core.models import Site

from v1.models.home_page import HomePage


class HomePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().get("/")
        cls.site_root = Site.objects.get(is_default_site=True).root_page

    def check_render_template(self, language, expected_template):
        page = HomePage(title="foo", slug="foo", language=language)
        self.site_root.add_child(instance=page)
        response = self.client.get("/foo/")
        self.assertEqual(response.template_name, expected_template)

    def test_render_english(self):
        self.check_render_template("en", "v1/home_page/home_page.html")

    def test_render_spanish_uses_legacy_template(self):
        self.check_render_template("es", "v1/home_page/home_page_legacy.html")

    def test_render_other_language_raises_exception(self):
        with self.assertRaises(NotImplementedError):
            self.check_render_template(
                "ar", "v1/home_page/home_page_legacy.html"
            )
