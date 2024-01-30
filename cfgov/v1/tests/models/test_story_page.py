from django.test import RequestFactory, TestCase

from v1.models import StoryPage


class StoryPageTests(TestCase):
    def test_story_page_excludes_breadcrumbs(self):
        def get_bread(request):
            return [1, 2, 3]

        page = StoryPage(title="test", slug="test")
        page.get_breadcrumbs = get_bread

        request = RequestFactory().get("/")
        response = page.serve(request)
        self.assertNotContains(response, "breadcrumbs_text")
