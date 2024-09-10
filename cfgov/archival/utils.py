import json
import logging

from django.apps import apps
from django.core.serializers.json import DjangoJSONEncoder
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone

from wagtail.coreutils import find_available_slug
from wagtail.models import get_streamfield_names


logger = logging.getLogger(__name__)


def get_last_migration(app):
    Migration = MigrationRecorder.Migration
    app_migrations = Migration.objects.filter(app=app).order_by("-applied")
    last_migration = app_migrations.first()

    if last_migration is None:
        return ""

    return last_migration.name


def export_page(page):
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

    logger.info(f"Exported {page.slug} to JSON")
    return page_json


def import_page(parent_page, page_json, slug=None):
    page_data = json.loads(page_json)

    # Verify that we can load import the page
    app_label = page_data["app_label"]
    model_name = page_data["model"]
    page_last_migration = page_data["last_migration"]

    # Get the specific model that the imported page belongs to
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError as exc:
        logger.error(
            f"Unable to import page of type {app_label}.{model_name}; {exc}"
        )
        raise

    # Compare the last migration
    last_migration = get_last_migration(app_label)
    if last_migration != page_last_migration:
        message = (
            f"Mismatched migrations: {app_label} is at {last_migration}, "
            f"page exported at {page_last_migration}"
        )
        logger.error(message)
        raise ValueError(message)

    # Construct a bare Page object first to get the treebeard
    # assignments right.
    # from_serializable_data comes from django-modelcluster
    page = model.from_serializable_data(page_data["data"])

    # Import with a different slug if a page already exists with the imported
    # slug.
    page.slug = find_available_slug(parent_page, page.slug)

    # These will all be set appropriate when we call add_child on parent_page
    page.path = None
    page.depth = None
    page.numchild = 0
    page.url_path = None

    # Reset the translation key
    # TODO: I doubt we want to do this, but it's useful in testing.
    # page.translation_key = uuid.uuid4()

    # All imported pages will be drafts by default
    page.live = False

    # Add the page to the parent
    parent_page.add_child(instance=page)

    logger.info(f"Imported {page.slug} as child of {parent_page.slug}")
    return page
