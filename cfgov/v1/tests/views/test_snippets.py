from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file

from taggit.models import Tag

from v1.models import Resource
from v1.views.snippets import ResourceTagsFilter, ThumbnailColumn


Image = get_image_model()


class ResourceTagsFilterTests(TestCase):
    def setUp(self):
        Tag.objects.bulk_create(
            Tag(name=tag, slug=tag) for tag in ["a", "b", "c"]
        )

        self.res1 = Resource.objects.create(title="1")

        self.res2 = Resource.objects.create(title="2")
        self.res2.tags.add("a")

        self.res3 = Resource.objects.create(title="3")
        self.res3.tags.add("a", "b")

    def test_default_filtering(self):
        f = ResourceTagsFilter()
        self.assertQuerysetEqual(f.queryset, Resource.objects.all())

    def test_filter_by_tags(self):
        f = ResourceTagsFilter({"tags": ["a"]})
        self.assertQuerysetEqual(f.queryset, Resource.objects.all())
        self.assertQuerysetEqual(
            f.qs, Resource.objects.filter(title__in=["2", "3"])
        )


class ThumbnailColumnTests(TestCase):
    def test_null_image_returns_empty_string(self):
        column = ThumbnailColumn("thumbnail", "width-100")
        resource = Resource(title="test")
        self.assertEqual(column.get_value(resource), "")

    def test_bad_attribute(self):
        column = ThumbnailColumn("missing", "width-100")
        resource = Resource(title="test")
        with self.assertRaises(ImproperlyConfigured) as e:
            column.get_value(resource)
        self.assertEqual(
            str(e.exception), "No attribute `missing` on class `Resource`."
        )

    def test_valid_thumbnail(self):
        column = ThumbnailColumn("thumbnail", "width-100")
        image = Image.objects.create(
            title="test",
            file=get_test_image_file(),
        )
        resource = Resource(title="Title", thumbnail=image)
        self.assertRegex(
            column.get_value(resource),
            (
                r'<img class="admin-thumb" decoding="async" loading="lazy" '
                r'src="/f/images/test.*\.width-100\.png">'
            ),
        )
