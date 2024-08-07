from urllib.parse import unquote

from django.apps import apps
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import smart_str

from wagtail import hooks

from fs import path
from portablepages.utils import export_page


def archive_page_data(page):
    fs = apps.get_app_config("archival").filesystem

    page_path = unquote(page.specific.url[1:])
    archive_path = path.join(settings.ARCHIVE_DIR, page_path)
    fs.exists(archive_path) or fs.makedirs(archive_path)

    page_json = export_page(page)

    now = timezone.now()
    page_filename = f"{page.slug}-{now.isoformat()}.json"
    target_path = smart_str(path.join(archive_path, page_filename))

    fs.writetext(target_path, page_json, encoding="utf8")


@hooks.register("before_delete_page")
def archive_before_deletion(request, page):
    """Archive a page before deleting it."""
    archive_page_data(page)
