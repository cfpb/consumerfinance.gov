import collections
import csv
import logging
import re

from django.apps import apps
from django.core.exceptions import FieldError
from django.core.management.base import BaseCommand

from wagtail.blocks.stream_block import StreamValue
from wagtail.models import Site, get_page_models


logger = logging.getLogger(__name__)


def find_pattern(data, pattern, key, path=None):
    """Return the path and match for a given regular expression in JSON

    For the given JSON-like data descend through the data structures looking
    for strings that match the `re.compile()`ed pattern.

    When one is found, the path to the match will be yielded along with any
    matching strings.

    If the path goes through a JSON array, it will include
    the index in the array.

    If the path goes through a JSON object, the value of the given "key" if
    it exists on the object will be used to identify it in the path.
    """
    if path is None:
        path = []

    # If it's a stririch textng, try to match it
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
            # "value" is implied in the path, any other key is explicit
            item_path = local_path + [item] if item != "value" else local_path
            yield from find_pattern(data[item], pattern, key, path=item_path)

    # If it's a sequence, iterate over its members
    elif isinstance(data, collections.Sequence) and not isinstance(data, str):
        for index, item in enumerate(data):
            local_path = path + [str(index)]
            yield from find_pattern(item, pattern, key, path=local_path)


class Command(BaseCommand):
    help = (
        "Search for a string or regular expression through page fields."
        "Pass a list in the form of app_name.page_type.field for each page "
        "type and field you want to report on. "
        "By default the report will include all page types and all text-based "
        "fields on the page."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--pagetype",
            action="append",
            help=(
                "Specify the page type(s) and field to check."
                "This should be given in the form app_name.page_type.field "
                "to include a page type in the given app with the given field."
                "For example, v1.BrowsePage.content."
            ),
        )
        parser.add_argument(
            "-s",
            "--search",
            required=True,
            help=(
                "The search string to match. This can be a regular expression."
            ),
        )

    def handle(self, *args, **options):
        writer = csv.writer(self.stdout)
        writer.writerow(
            (
                "Page ID",
                "Page Type",
                "Page Title",
                "Page URL",
                "Field",
                "Stream Field Path",
                "Stream Field Matches",
            )
        )

        search_string = options["search"]
        search_re = re.compile(search_string, re.MULTILINE | re.DOTALL)

        pagetypes = options["pagetype"]
        if pagetypes is None:
            pagetypes = self.get_all_page_models_and_fields()

        for app_name_page_type_field in pagetypes:
            app_name, page_type, field = app_name_page_type_field.split(".")
            for match_data in self.get_matches(
                search_re, app_name, page_type, field
            ):
                writer.writerow(match_data)

    def prepare_pattern_for_database(self, pattern):
        return pattern.replace('"', r'\\"')

    def get_all_page_models_and_fields(self):
        page_models = get_page_models()

        pagetypes = []
        for page_model in page_models:
            for field in page_model._meta.concrete_fields:
                pagetypes.append(
                    f"{page_model._meta.app_label}."
                    f"{page_model._meta.object_name}."
                    f"{field.name}"
                )

        return pagetypes

    def get_matches(self, search_re, app_name, page_type, field):
        PageModel = apps.get_model(app_label=app_name, model_name=page_type)

        site = Site.objects.get(is_default_site=True)

        # Search for live pages in the default site
        queryset = PageModel.objects.live().in_site(site)

        # Try to do regular expression-matching of the search string.
        # If that doesn't work, warn and fall back on icontains
        try:
            queryset = queryset.filter(
                **{
                    f"{field}__iregex": self.prepare_pattern_for_database(
                        search_re.pattern
                    )
                }
            )
        except FieldError:
            logging.debug(f"Cannot search {app_name}.{page_type}.{field}.")
            return

        # Get only exact matches for the page model
        queryset = queryset.exact_type(PageModel)

        for p in queryset:
            field_value = getattr(p, field)

            match_row = [
                p.id,
                page_type,
                p.title,
                p.get_url(),
                field,
            ]

            if isinstance(field_value, StreamValue):
                # If this field is a StreamField, dive into it to get paths
                # and matches
                for streamfield_path, matches in find_pattern(
                    field_value.raw_data, search_re, "type"
                ):
                    yield match_row + [".".join(streamfield_path), *matches]
            else:
                # Otherwise, just return the field
                yield match_row
