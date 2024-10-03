import json
import logging
import os.path
import re
from urllib.parse import unquote

from django.apps import apps
from django.core.files.base import ContentFile
from django.core.files.storage import InvalidStorageError, storages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone
from django.utils.encoding import smart_str

from wagtail.coreutils import find_available_slug
from wagtail.models import get_streamfield_names


logger = logging.getLogger(__name__)


def get_archive_storage():
    try:
        return storages["wagtail_deletion_archival"]
    except InvalidStorageError:
        return None


def get_last_migration(app):
    Migration = MigrationRecorder.Migration
    app_migrations = Migration.objects.filter(app=app).order_by("-applied")
    last_migration = app_migrations.first()

    if last_migration is None:
        return ""

    return last_migration.name


def convert_page_to_json(page):
    """Get a copy of the page as JSON."""

    # This includes its app_label, model, and the latest migration applied for
    # the app, allowing any import to quickly verify whether import is
    # possible (due to app or model availability and/or schema changes).
    page_export = {
        "app_label": page.content_type.app_label,
        "model": page.content_type.model,
        "last_migration": get_last_migration(page.content_type.app_label),
        "exported_at": timezone.now().isoformat(),
    }

    # The serializable_data comes from django-modelcluster.
    page_export["data"] = page.serializable_data()

    # Convert streamfields, which serialize as strings containing JSON, back
    # into objects. This will keep the final JSON cleaner, and not with
    # JSON-in-a-string-in-JSON
    streamfield_names = get_streamfield_names(page.specific.__class__)
    for streamfield_name in streamfield_names:
        page_export["data"][streamfield_name] = json.loads(
            page_export["data"][streamfield_name]
        )

    # Strip the pk out of the data so that, on import, from_serializable_data()
    # always creates a new object.
    page_export["data"]["pk"] = None

    # Dump the page data to JSON
    page_json = json.dumps(
        page_export, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder
    )

    return page_json


def make_archive_filename(page_slug):
    now = timezone.now()
    return f"{page_slug}-{now.isoformat()}.json"


ARCHIVE_FILENAME_RE = re.compile(
    # Starting with any character then -
    r"^.+-"
    # YYYY-MM-DDTHH:MM:SS
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    # Optional .ffffff
    r"(\.[0-9]{1,6})?"
    # Optional timezone
    r"([+-][0-9]{2}:[0-9]{2})?"
    # .json
    r"\.json$"
)


def export_page_signal_handler(sender, instance, **kwargs):
    archive_storage = get_archive_storage()

    if not archive_storage:
        return

    page = instance.specific
    site = page.get_site()
    page_path = unquote(page.relative_url(site)).lstrip("/")

    page_json = convert_page_to_json(page)

    page_filename = make_archive_filename(page.slug)
    target_path = smart_str(os.path.join(page_path, page_filename))

    archived_filename = archive_storage.save(
        target_path, ContentFile(page_json.encode("utf-8"))
    )
    logger.info(f"Exported {page.slug} to JSON at {archived_filename}")


def import_page(parent_page, page_json):
    page_data = json.loads(page_json)

    # Verify that we can load import the page
    app_label = page_data["app_label"]
    model_name = page_data["model"]

    # Get the specific model that the imported page belongs to.
    # This will raise a `LookupError` if the app/model doesn't exist, which
    # we'll let percolate up.
    model = apps.get_model(app_label, model_name)

    # Construct a bare Page object first to get the treebeard
    # assignments right.
    # from_serializable_data comes from django-modelcluster
    page = model.from_serializable_data(page_data["data"])

    # Import with a different slug if a page already exists with the imported
    # slug.
    page.slug = find_available_slug(parent_page, page.slug)

    # These will all be set appropriately when we call add_child on parent_page
    page.path = None
    page.depth = None
    page.numchild = 0
    page.url_path = None

    # All imported pages will be drafts by default
    page.live = False

    # Add the page to the parent
    parent_page.add_child(instance=page)

    logger.info(f"Imported {page.slug} as child of {parent_page.slug}")
    return page
