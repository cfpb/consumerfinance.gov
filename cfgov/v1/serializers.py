from operator import itemgetter

from django.conf import settings

from rest_framework import serializers

from v1.jinja2tags.images import image_alt_value, wagtail_image_fn
from v1.models import CFGOVPageCategory, EventPage
from v1.util.ref import get_category_icon, is_blog, is_report


class FilterPageSerializer(serializers.Serializer):
    authors = serializers.ListField(source="get_authors")
    categories = serializers.SerializerMethodField()
    date_published = serializers.ReadOnlyField()
    event_location_str = serializers.SerializerMethodField()
    full_url = serializers.SerializerMethodField()
    image_alt = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    is_blog = serializers.SerializerMethodField()
    is_event = serializers.SerializerMethodField()
    is_report = serializers.SerializerMethodField()
    language = serializers.ChoiceField(choices=settings.LANGUAGES)
    page_id = serializers.ReadOnlyField(source="id")
    preview_title = serializers.SerializerMethodField()
    search_description = serializers.ReadOnlyField()
    start_date = serializers.SerializerMethodField()
    title = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_categories(self, page):
        category_mapping = dict(CFGOVPageCategory.name.field.flatchoices)

        categories = []
        for category in page.categories.all():
            category_slug = category.name
            category_name = category_mapping[category_slug]
            categories.append(
                {
                    "slug": category_slug,
                    "name": category_name,
                    "icon": get_category_icon(category_name),
                }
            )

        return sorted(categories, key=itemgetter("name"))

    def get_event_location_str(self, page):
        return page.location_str if isinstance(page, EventPage) else None

    def get_full_url(self, page):
        return page.get_full_url(request=self.context.get("request"))

    def get_image_alt(self, page):
        if (
            isinstance(page, EventPage)
            and page.venue_image_type == "image"
            and page.venue_image
        ):
            return image_alt_value(page.venue_image)

        return ""

    def get_image_url(self, page):
        if isinstance(page, EventPage):
            if page.venue_image_type == "map":
                return page.location_image_url()
            if page.venue_image_type == "image" and page.venue_image:
                rendition = wagtail_image_fn(page.venue_image, "width-540")
                return rendition.url

    def get_is_blog(self, page):
        return is_blog(page)

    def get_is_event(self, page):
        return isinstance(page, EventPage)

    def get_is_report(self, page):
        return is_report(page)

    def get_preview_title(self, page):
        return page.seo_title or page.title

    def get_start_date(self, page):
        return getattr(page, page.start_date_field)

    def get_url(self, page):
        return page.get_url(request=self.context.get("request"))

    def get_tags(self, page):
        tags = [
            {
                "slug": tag.slug,
                "text": tag.name,
                "url": f"?topics={tag.slug}",
            }
            for tag in page.tags.all()
        ]

        return sorted(tags, key=itemgetter("text"))
