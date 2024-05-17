from datetime import date

from django.test import RequestFactory

from wagtail.models import Site

from core.testutils.test_cases import WagtailPageTreeTestCase
from v1.models import BlogPage, CFGOVPageCategory
from v1.models.learn_page import AbstractFilterPage
from v1.serializers import FilterPageSerializer


class FilterablePageSerializerTests(WagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        return [
            BlogPage(title=f"child{i}", date_published=date(2000, 1, 2))
            for i in range(10)
        ]

    def setUp(self):
        self.request = RequestFactory().get("/")

        # Deliberately pre-cache Site root paths on the request object
        # so we don't need to make database queries for these later.
        site = Site.find_for_request(self.request)
        site.root_page._get_site_root_paths(self.request)

        for i in range(10):
            page = BlogPage.objects.get(slug=f"child{i}")
            page.authors.add("Famous Author", "Another Person")
            page.save()

            for category_name in ["at-the-cfpb", "auto-loans"]:
                CFGOVPageCategory.objects.create(page=page, name=category_name)

    def test_serialization(self):
        queryset = AbstractFilterPage.objects.prefetch_related(
            "authors", "categories", "tags"
        ).specific()

        serializer = FilterPageSerializer(
            queryset, many=True, context={"request": self.request}
        )

        # Fetching BlogPages and related objects takes 4 queries:
        #
        # 1. Fetching the base Page objects from the database.
        # 2. Fetching the specific BlogPage objects from the database.
        # 3. Fetching Page authors from the database, done as a single query
        #    using prefetch_related above.
        # 4. Fetching Page categories from the database, done as a single query
        #    using prefetch_related above.
        #
        # The serializing itself shouldn't take any additional queries,
        # assuming the fetching is implemented as above.
        with self.assertNumQueries(4):
            data = serializer.data

        self.assertEqual(
            data,
            [
                {
                    "authors": [
                        "Famous Author",
                        "Another Person",
                    ],
                    "categories": [
                        {
                            "slug": "at-the-cfpb",
                            "name": "At the CFPB",
                            "icon": "bullhorn",
                        },
                        {
                            "slug": "auto-loans",
                            "name": "Auto loans",
                            "icon": "car",
                        },
                    ],
                    "language": "en",
                    "start_date": date(2000, 1, 2),
                    "title": f"child{i}",
                    "url": f"/child{i}/",
                }
                for i in range(10)
            ],
        )
