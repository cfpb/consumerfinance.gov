from datetime import date

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

    def assertSerialization(self, page, expected):
        self.root_page.add_child(instance=page)
        serializer = FilterPageSerializer(
            page, context={"request": self.request}
        )
        self.assertDictEqual(serializer.data, expected)

    def test_blog_serialization(self):
        blog = BlogPage(title="Blog", date_published=date(2024, 1, 1))
        blog.authors.add(
            "Mark Twain",
            "William Shakespeare",
        )
        blog.categories.add(
            CFGOVPageCategory(name="info-for-consumers"),
            CFGOVPageCategory(name="at-the-cfpb"),
        )
        blog.tags.add("Mortgages", "Payments")

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
                "event_location_str": None,
                "image_alt": None,
                "image_url": None,
                "is_blog": True,
                "is_event": False,
                "is_report": False,
                "language": "en",
                "start_date": date(2024, 1, 1),
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
        now = timezone.now()
        event = EventPage(title="Event", start_dt=now, venue_image_type="none")

        self.assertSerialization(
            event,
            {
                "authors": [],
                "categories": [],
                "event_location_str": "",
                "image_alt": None,
                "image_url": None,
                "is_blog": False,
                "is_event": True,
                "is_report": False,
                "language": "en",
                "start_date": now.date(),
                "tags": [],
                "title": "Event",
                "url": "/event/",
            },
        )

    def test_event_serialization_with_map_image(self):
        now = timezone.now()
        event = EventPage(
            title="Event",
            start_dt=now,
            venue_name="CFPB HQ",
            venue_image_type="map",
        )

        self.assertSerialization(
            event,
            {
                "authors": [],
                "categories": [],
                "event_location_str": "CFPB HQ",
                "image_alt": None,
                "image_url": (
                    "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
                    "-77.039628,38.898238,12/276x155?access_token=None"
                ),
                "is_blog": False,
                "is_event": True,
                "is_report": False,
                "language": "en",
                "start_date": now.date(),
                "tags": [],
                "title": "Event",
                "url": "/event/",
            },
        )

    def test_event_serialization_with_venue_image(self):
        now = timezone.now()
        image = CFGOVImage.objects.create(
            title="Venue image",
            file=get_test_image_file(),
            alt="Venue image alt text",
        )
        event = EventPage(
            title="Event",
            start_dt=now,
            venue_image_type="image",
            venue_image=image,
        )

        self.assertSerialization(
            event,
            {
                "authors": [],
                "categories": [],
                "event_location_str": "",
                "image_alt": "Venue image alt text",
                "image_url": "/f/images/test.width-540.png",
                "is_blog": False,
                "is_event": True,
                "is_report": False,
                "language": "en",
                "start_date": now.date(),
                "tags": [],
                "title": "Event",
                "url": "/event/",
            },
        )
