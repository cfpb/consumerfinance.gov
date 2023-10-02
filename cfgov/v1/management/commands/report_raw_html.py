import collections
import csv
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from wagtail.models import Site, get_page_models


def find_pattern(data, pattern, key, path=None):
    """Return the path and match for a given regular expression in JSON

    For the given JSON-like data descend through the data structures looking
    for strings that match the `re.compile()`ed pattern.

    When one is found, the path to the match will be yielded along with any
    matching strings.

    If the path goes through a a JSON array, it will include
    the index in the array.

    If the path goes through a JSON object, the value of the given "key" if
    it exists on the object will be used to idenfiy it in the path."""
    if path is None:
        path = []

    # If it's a string, try to match it
    if isinstance(data, str):
        matches = pattern.findall(data)
        if len(matches) > 0:
            yield path, matches

    # If it's a mapping, iterate over its key/value pairs
    elif isinstance(data, collections.Mapping):
        local_path = path
        if key in data:
            local_path = path + [data[key]]

        for item in data:
            yield from find_pattern(data[item], pattern, key, path=local_path)

    # If it's a sequence, iterate over its members
    elif isinstance(data, collections.Sequence) and not isinstance(data, str):
        for index, item in enumerate(data):
            local_path = path + [str(index)]
            yield from find_pattern(item, pattern, key, path=local_path)


class Command(BaseCommand):
    help = (
        "Discover raw HTML tags within &lt; &gt; entities in page fields. "
        "Pass a list in the form of app_name.page_type.field for each page "
        "type and field you want to report on."
    )

    # Match "&lt;" followed by any 0 or more characters that are not "&gt;",
    # followed by "&gt;" This should match HTML that's encoded in HTML entities
    # in the given fields.
    html_tag_entity_pattern = r"&lt;[a-zA-Z]+(?!&gt;).*?&gt;"
    html_tag_entity_re = re.compile(
        html_tag_entity_pattern, re.MULTILINE | re.DOTALL
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "pagetype",
            nargs="*",
            help=(
                "Specify the page type(s) and field to check."
                "This should be given in the form app_name.page_type.field "
                "to include a page type in the given app with the given field."
                "For example, v1.BrowsePage.content."
            ),
        )

    def handle(self, *args, **options):
        raw_html_writer = csv.writer(self.stdout)
        raw_html_writer.writerow(
            (
                "Page ID",
                "Page Type",
                "Page Title",
                "Page URL",
                "Raw HTML Block Path",
                "Raw HTML",
            )
        )

        pagetypes = options["pagetype"]
        if len(pagetypes) == 0:
            pagetypes = self.get_all_page_models_and_stream_fields()

        for app_name_page_type_field in pagetypes:
            app_name, page_type, field = app_name_page_type_field.split(".")
            for match_data in self.get_matches(app_name, page_type, field):
                raw_html_writer.writerow(match_data)

    def get_all_page_models_and_stream_fields(self):
        page_models = get_page_models()

        pagetypes = []
        for page_model in page_models:
            for streamfield_name in page_model.get_streamfield_names():
                pagetypes.append(
                    f"{page_model._meta.app_label}."
                    f"{page_model._meta.object_name}."
                    f"{streamfield_name}"
                )

        return pagetypes

    def get_matches(self, app_name, page_type, field):
        field_filter = {f"{field}__iregex": self.html_tag_entity_pattern}
        PageModel = apps.get_model(app_label=app_name, model_name=page_type)

        site = Site.objects.get(is_default_site=True)
        queryset = (
            PageModel.objects.live()
            .in_site(site)
            .filter(**field_filter)
            .exact_type(PageModel)
        )

        for p in queryset:
            json_field = getattr(p, field)

            for path, matches in find_pattern(
                json_field.raw_data, self.html_tag_entity_re, "type"
            ):
                yield [
                    p.id,
                    page_type,
                    p.title,
                    p.get_url(),
                    ".".join(path),
                ] + matches
