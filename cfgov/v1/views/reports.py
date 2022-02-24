from datetime import date

from wagtail.admin.views.reports import PageReportView, ReportView
from wagtail.documents.models import Document

from v1.models import CFGOVPage


def process_categories(queryset):
    """Prep the set of categories associated with a page."""
    return ", ".join([cat.get_name_display() for cat in queryset])


def process_tags(queryset):
    """Prep the set of tags assocaited with a document or page."""
    return ", ".join([tag for tag in queryset])


def construct_absolute_url(url):
    """Turn a relativey URL into an absolute URL"""
    return "https://www.consumerfinance.gov" + url


class PageMetadataReportView(PageReportView):
    header_icon = "doc-empty-inverse"
    title = "Metadata for live pages"

    list_export = PageReportView.list_export + [
        "url",
        "first_published_at",
        "last_published_at",
        "language",
        "search_description",
        "tags.names",
        "categories.all",
    ]
    export_headings = dict([
        ("url", "URL"),
        ("first_published_at", "First published"),
        ("last_published_at", "Last published"),
        ("language", "Language"),
        ("search_description", "Search description"),
        ("tags.names", "Tags"),
        ("categories.all", "Categories")],
        **PageReportView.export_headings,
    )

    custom_field_preprocess = {
        "categories.all": {
            "csv": process_categories, "xlsx": process_categories
        }
    }

    template_name = "v1/page_metadata_report.html"

    def get_filename(self):
        """ Get a dated base filename for the exported spreadsheet."""
        return f"spreadsheet-export-{date.today()}"

    def get_queryset(self):
        return CFGOVPage.objects.filter(live=True).prefetch_related(
            "tags", "categories")


class DocumentsReportView(ReportView):
    header_icon = "doc-full"
    title = "All documents"

    list_export = [
        "id",
        "title",
        "filename",
        "url",
        "collection",
        "tags.names",
        "created_at",
        "uploaded_by_user",
    ]
    export_headings = {
        "id": "ID",
        "title": "Title",
        "filename": "File",
        "url": "URL",
        "collection": "Collection",
        "tags.names": "Tags",
        "created_at": "Uploaded on",
        "uploaded_by_user": "Uploaded by",
    }

    custom_field_preprocess = {
        "tags.names": {
            "csv": process_tags
        },
        "url": {
            "csv": construct_absolute_url
        }
    }

    template_name = "v1/documents_report.html"

    def get_filename(self):
        """ Get a better filename than the default 'spreadsheet-export'. """
        return f"all-cfgov-documents-{date.today()}"

    def get_queryset(self):
        return Document.objects.all().order_by('-id').prefetch_related(
            "tags")
