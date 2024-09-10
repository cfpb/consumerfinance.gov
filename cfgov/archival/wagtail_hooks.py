from urllib.parse import unquote

from django.apps import apps
from django.conf import settings
from django.db.models.signals import pre_delete
from django.urls import path as django_path
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_str

from wagtail import hooks
from wagtail.admin.widgets import Button

from fs import path as fs_path

from archival.utils import export_page
from archival.views import export_view, import_view


def archive_page_data_receiver(sender, instance, **kwargs):
    # If settings.ARCHIVE_FILESYSTEM is not set, don't do anything
    if getattr(settings, "ARCHIVE_FILESYSTEM", None) is None:
        return

    fs = apps.get_app_config("archival").filesystem

    page = instance.specific

    page_path = unquote(page.url[1:])
    fs.exists(page_path) or fs.makedirs(page_path)

    page_json = export_page(page)

    now = timezone.now()
    page_filename = f"{page.slug}-{now.isoformat()}.json"
    target_path = smart_str(fs_path.join(page_path, page_filename))

    fs.writetext(target_path, page_json, encoding="utf8")


@hooks.register("before_delete_page")
def add_archival_signal_reciever(request, page):
    from wagtail.models import Page

    pre_delete.connect(archive_page_data_receiver, sender=Page)


@hooks.register("after_delete_page")
def remove_archival_signal_reciever(request, page):
    from wagtail.models import Page

    pre_delete.disconnect(archive_page_data_receiver, sender=Page)


@hooks.register("before_bulk_action")
def add_bulk_delete_signal_reciever(
    request, action_type, objects, action_class_instance
):
    from wagtail.models import Page

    if action_type == "delete":
        pre_delete.connect(archive_page_data_receiver, sender=Page)


@hooks.register("after_bulk_action")
def remove_bulk_delete_signal_reciever(
    request, action_type, objects, action_class_instance
):
    from wagtail.models import Page

    if action_type == "delete":
        pre_delete.disconnect(archive_page_data_receiver, sender=Page)


@hooks.register("register_page_listing_more_buttons")
def page_export_button(
    page,
    page_perms,
    is_parent=False,
    next_url=None,
):
    yield Button(
        "Export",
        reverse("export_page", args=(page.id,)),
        priority=210,
        icon_name="download",
    )


@hooks.register("register_page_header_buttons")
def page_import_button(page, user, view_name, next_url=None):
    yield Button(
        "Import",
        reverse("import_page", args=(page.id,)),
        priority=200,
        icon_name="upload",
    )


@hooks.register("register_admin_urls")
def register_portable_page_admin_urls():
    return [
        django_path("export/<int:page_id>/", export_view, name="export_page"),
        django_path("import/<int:page_id>/", import_view, name="import_page"),
    ]
