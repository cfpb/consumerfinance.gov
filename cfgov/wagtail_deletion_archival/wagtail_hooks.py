from django.db.models.signals import pre_delete
from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.widgets import Button
from wagtail.models import Page

from wagtail_deletion_archival.utils import export_page_signal_handler
from wagtail_deletion_archival.views import (
    ArchiveFileView,
    ArchiveIndexView,
    import_view,
)


@hooks.register("register_page_header_buttons")
def page_import_button(page, user, view_name, next_url=None):
    yield Button(
        "Import",
        reverse("wagtail_deletion_archive_import", args=(page.id,)),
        priority=200,
        icon_name="upload",
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    archive_url_prefix = "__deleted/"

    return [
        path(
            "import/<int:page_id>/",
            import_view,
            name="wagtail_deletion_archive_import",
        ),
        path(
            archive_url_prefix,
            ArchiveIndexView.as_view(),
            name="wagtail_deletion_archive_index",
        ),
        path(
            f"{archive_url_prefix}<path:path>",
            ArchiveFileView.as_view(),
            name="wagtail_deletion_archive_serve",
        ),
    ]


@hooks.register("before_delete_page")
def add_archival_signal_reciever(request, page):
    pre_delete.connect(export_page_signal_handler, sender=Page)


@hooks.register("after_delete_page")
def remove_archival_signal_reciever(request, page):
    pre_delete.disconnect(export_page_signal_handler, sender=Page)


@hooks.register("before_bulk_action")
def add_bulk_delete_signal_reciever(
    request, action_type, objects, action_class_instance
):
    if action_type == "delete":
        pre_delete.connect(export_page_signal_handler, sender=Page)


@hooks.register("after_bulk_action")
def remove_bulk_delete_signal_reciever(
    request, action_type, objects, action_class_instance
):
    if action_type == "delete":
        pre_delete.disconnect(export_page_signal_handler, sender=Page)
