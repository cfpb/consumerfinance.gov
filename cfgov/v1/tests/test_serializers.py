from django.test import RequestFactory, TestCase
from django.utils import timezone

from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Site

from v1.models import BlogPage, CFGOVImage, CFGOVPageCategory, EventPage
from v1.serializers import FilterPageSerializer


class FilterablePageSerializerTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.now = timezone.now()
        self.today = self.now.date()

    def assertSerialization(self, page, expected):
        self.root_page.add_child(instance=page)
        serializer = FilterPageSerializer(
            page, context={"request": self.request}
        )
        self.assertDictEqual(serializer.data, expected)

    def test_blog_serialization(self):
        blog = BlogPage(
            pk=123,
            title="Blog",
            seo_title="Read this blog!",
            date_published=self.today,
            search_description="A blog post",
        )
        blog.authors.add(
            "Mark Twain",
            "William Shakespeare",
        )
        blog.categories.add(
            CFGOVPageCategory(name="info-for-consumers"),
            CFGOVPageCategory(name="at-the-cfpb"),
        )
        blog.tags.add("Payments", "Mortgages")

        self.assertSerialization(
            blog,
            {
                "authors": ["William Shakespeare", "Mark Twain"],
                "categories": [
                    {
                        "icon": "bullhorn",
                        "name": "At the CFPB",
                        "slug": "at-the-cfpb",
                    },
                    {
                        "icon": "information",
                        "name": "Info for consumers",
                        "slug": "info-for-consumers",
                    },
                ],
                "date_published": self.today,
                "event_location_str": None,
                "full_url": "http://localhost/blog/",
                "image_alt": "",
                "image_url": None,
                "is_blog": True,
                "is_event": False,
                "is_report": False,
                "language": "en",
                "page_id": 123,
                "preview_title": "Read this blog!",
                "search_description": "A blog post",
                "start_date": self.today,
                "tags": [
                    {
                        "slug": "mortgages",
                        "text": "Mortgages",
                        "url": "?topics=mortgages",
                    },
                    {
                        "slug": "payments",
                        "text": "Payments",
                        "url": "?topics=payments",
                    },
                ],
                "title": "Blog",
                "url": "/blog/",
            },
        )

    def test_event_serialization_no_image(self):
        event = EventPage(
            pk=123,
            title="Event",
            date_published=self.today,
            start_dt=self.now,
            venue_image_type="none",
        )

        self.assertSerialization(
            event,
            {
                "authors": [],
                "categories": [],
                "date_published": self.today,
                "event_location_str": "",
                "full_url": "http://localhost/event/",
                "image_alt": "",
                "image_url": None,
                "is_blog": False,
                "is_event": True,
                "is_report": False,
                "language": "en",
                "page_id": 123,
                "preview_title": "Event",
                "search_description": "",
                "start_date": self.now,
                "tags": [],
                "title": "Event",
                "url": "/event/",
            },
        )

    def test_event_serialization_with_map_image(self):
        event = EventPage(
            pk=123,
            title="Event",
            date_published=self.today,
            start_dt=self.now,
            venue_name="CFPB HQ",
            venue_image_type="map",
        )

        self.assertSerialization(
            event,
            {
                "authors": [],
                "categories": [],
                "date_published": self.today,
                "event_location_str": "CFPB HQ",
                "full_url": "http://localhost/event/",
                "image_alt": "",
                "image_url": (
                    "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
                    "-77.039628,38.898238,12/276x155?access_token=None"
                ),
                "is_blog": False,
                "is_event": True,
                "is_report": False,
                "language": "en",
                "page_id": 123,
                "preview_title": "Event",
                "search_description": "",
                "start_date": self.now,
                "tags": [],
                "title": "Event",
                "url": "/event/",
            },
        )

    def test_event_serialization_with_venue_image(self):
        image = CFGOVImage.objects.create(
            title="Venue image",
            file=get_test_image_file(filename="event-serialization.png"),
            alt="Venue image alt text",
        )
        event = EventPage(
            pk=123,
            title="Event",
            date_published=self.today,
            start_dt=self.now,
            venue_image_type="image",
            venue_image=image,
        )

        self.assertSerialization(
            event,
            {
                "authors": [],
                "categories": [],
                "date_published": self.today,
                "event_location_str": "",
                "full_url": "http://localhost/event/",
                "image_alt": "Venue image alt text",
                "image_url": "/f/images/event-serialization.width-540.png",
                "is_blog": False,
                "is_event": True,
                "is_report": False,
                "language": "en",
                "page_id": 123,
                "preview_title": "Event",
                "search_description": "",
                "start_date": self.now,
                "tags": [],
                "title": "Event",
                "url": "/event/",
            },
        )
