import os.path

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, reverse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.views.generic import View

from wagtail.admin.views.reports import ReportView
from wagtail.models import Page

from wagtail_deletion_archival.forms import ImportForm
from wagtail_deletion_archival.utils import (
    ARCHIVE_FILENAME_RE,
    get_archive_storage,
    import_page,
)


def import_view(request, page_id):
    parent_page = get_object_or_404(Page, id=page_id).specific

    if request.method == "POST":
        input_form = ImportForm(request.POST, request.FILES)

        if input_form.is_valid():
            json_file = request.FILES["page_file"]
            try:
                new_page = import_page(
                    parent_page, json_file.read().decode("utf8")
                )
            except Exception:
                input_form.add_error(
                    "page_file",
                    "There was an error importing this file as a page. "
                    "Please ensure the app and model it references exist, "
                    "and that its schema is up to date.",
                )
            else:
                return redirect("wagtailadmin_pages:edit", new_page.id)
    else:
        input_form = ImportForm()

    return TemplateResponse(
        request,
        "wagtail_deletion_archival/import_page.html",
        {
            "parent_page": parent_page,
            "form": input_form,
        },
    )


class ArchiveStorageViewMixin:
    def dispatch(self, *args, **kwargs):
        if not (storage := get_archive_storage()):
            raise Http404

        self.storage = storage
        return super().dispatch(*args, **kwargs)


class ArchiveLink:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            reverse(
                "wagtail_deletion_archive_serve",
                kwargs={"path": self.path},
            ),
            self.path,
        )


class ArchiveIndexView(ArchiveStorageViewMixin, ReportView):
    page_title = "Deleted Wagtail pages"

    def get_queryset(self):
        return list(map(ArchiveLink, self.get_archive_files_recursive()))

    def get_archive_files_recursive(self, path=""):
        archive_files = []

        dirs, filenames = self.storage.listdir(path)

        for filename in filenames:
            filename_path = os.path.join(path, filename)
            if ARCHIVE_FILENAME_RE.match(filename_path):
                archive_files.append(filename_path)

        for dir in dirs:
            archive_files.extend(
                self.get_archive_files_recursive(os.path.join(path, dir))
            )

        return archive_files


class ArchiveFileView(ArchiveStorageViewMixin, View):
    def get(self, request, path):
        if not ARCHIVE_FILENAME_RE.match(path) or not self.storage.exists(
            path
        ):
            raise Http404

        return FileResponse(self.storage.open(path), as_attachment=True)
