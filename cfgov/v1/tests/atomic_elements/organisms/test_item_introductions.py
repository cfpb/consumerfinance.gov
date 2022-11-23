from django.test import TestCase

from wagtail.core.models import Site

from v1.atomic_elements.organisms import ItemIntroduction
from v1.models import BlogPage, BrowseFilterablePage, CFGOVPageCategory


class ItemIntroductionTests(TestCase):
    def test_renders_category_link(self):
        site_root = Site.objects.get(is_default_site=True).root_page

        filter_page = BrowseFilterablePage(title="blog", slug="blog")
        site_root.add_child(instance=filter_page)

        child_page = BlogPage(title="post", slug="post")
        child_page.categories.add(CFGOVPageCategory(name="press-release"))
        filter_page.add_child(instance=child_page)

        block = ItemIntroduction()
        value = block.to_python(
            {
                "heading": "Heading",
                "show_category": True,
            }
        )
        html = block.render(value, context={"page": child_page})

        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn('<a href="/blog/?categories=press-release', html)
        self.assertIn("Press release", html)
