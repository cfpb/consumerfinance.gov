import json
from urllib.parse import unquote

from django.apps import apps
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import smart_str

from wagtail import hooks
from wagtail.models import get_streamfield_names

from fs import path


def export_page(page):
    page_data = {
        "app_label": page.content_type.app_label,
        "model": page.content_type.model,
        "path": page.specific.url,
        "data": page.serializable_data(),
    }

    # Convert streamfields, which serialize as strings containing JSON, back
    # into objects. This will keep the final JSON cleaner, and not with
    # JSON-in-a-string-in-JSON
    streamfield_names = get_streamfield_names(page.specific.__class__)
    for streamfield_name in streamfield_names:
        page_data["data"][streamfield_name] = json.loads(
            page_data["data"][streamfield_name]
        )

    page_json = json.dumps(
        page_data, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder
    )
    return page_json


def archive_page_data(page):
    fs = apps.get_app_config("archival").filesystem

    page_path = unquote(page.specific.url[1:])
    archive_path = path.join(settings.ARCHIVE_DIR, page_path)
    fs.exists(archive_path) or fs.makedirs(archive_path)

    page_json = export_page(page)
    page_filename = f"{page.slug}.json"
    target_path = smart_str(path.join(archive_path, page_filename))

    fs.writetext(target_path, page_json, encoding="utf8")


@hooks.register("before_delete_page")
def archive_before_deletion(request, page):
    """Archive a page with wagtail-bakery before deleting it."""
    archive_page_data(page)
