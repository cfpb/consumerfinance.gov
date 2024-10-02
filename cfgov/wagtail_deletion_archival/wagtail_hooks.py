from django.conf import settings
from django.db.models.signals import pre_delete
from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.widgets import Button

from wagtail_deletion_archival.utils import (
    export_page_signal_handler,
    get_archive_storage,
)
from wagtail_deletion_archival.views import (
    ArchiveFileView,
    ArchiveIndexView,
    import_view,
)


@hooks.register("register_admin_urls")
def register_archive_storage_import_url():
    return [
        path("import/<int:page_id>/", import_view, name="import_page"),
    ]


@hooks.register("register_page_header_buttons")
def page_import_button(page, user, view_name, next_url=None):
    yield Button(
        "Import",
        reverse("import_page", args=(page.id,)),
        priority=200,
        icon_name="upload",
    )


if get_archive_storage():

    @hooks.register("register_admin_urls")
    def register_deleted_page_archive_list_url():
        return [
            path(
                settings.WAGTAIL_DELETION_ARCHIVE_URL,
                ArchiveIndexView.as_view(),
            ),
            path(
                f"{settings.WAGTAIL_DELETION_ARCHIVE_URL}<path:path>",
                ArchiveFileView.as_view(),
                name="wagtail_deletion_archive_serve",
            ),
        ]

    @hooks.register("before_delete_page")
    def add_archival_signal_reciever(request, page):
        from wagtail.models import Page

        pre_delete.connect(export_page_signal_handler, sender=Page)

    @hooks.register("after_delete_page")
    def remove_archival_signal_reciever(request, page):
        from wagtail.models import Page

        pre_delete.disconnect(export_page_signal_handler, sender=Page)

    @hooks.register("before_bulk_action")
    def add_bulk_delete_signal_reciever(
        request, action_type, objects, action_class_instance
    ):
        from wagtail.models import Page

        if action_type == "delete":
            pre_delete.connect(export_page_signal_handler, sender=Page)

    @hooks.register("after_bulk_action")
    def remove_bulk_delete_signal_reciever(
        request, action_type, objects, action_class_instance
    ):
        from wagtail.models import Page

        if action_type == "delete":
            pre_delete.disconnect(export_page_signal_handler, sender=Page)
