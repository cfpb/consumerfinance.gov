from datetime import date

from wagtail.admin.views.reports import PageReportView

from v1.models import CFGOVPage


def process_categories(queryset):
    """Prep the set of categories associated with a page."""
    return ", ".join([cat.get_name_display() for cat in queryset])


class PageMetadataReportView(PageReportView):
    header_icon = "doc-empty-inverse"
    title = "Metadata for live pages"

    list_export = PageReportView.list_export + [
        "url",
        "first_published_at",
        "last_published_at",
        "search_description",
        "tags.names",
        "categories.all",
    ]
    export_headings = dict([
        ("url", "URL"),
        ("first_published_at", "First published"),
        ("last_published_at", "Last published"),
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
