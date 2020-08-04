from wagtail.admin.views.reports import PageReportView

from v1.models import CFGOVPage


class PageMetadataReportView(PageReportView):
    header_icon = 'doc-empty-inverse'
    title = "Metadata for live pages"

    list_export = PageReportView.list_export + [
        'url',
        'first_published_at',
        'last_published_at',
        'search_description'
    ]
    export_headings = dict(
        url='URL',
        first_published_at='First published',
        last_published_at='Last published',
        search_description='Search description',
        **PageReportView.export_headings
    )

    template_name = 'v1/page_metadata_report.html'

    def get_queryset(self):
        # We don't really need test coverage of the object manger
        return CFGOVPage.objects.filter(live=True)  # pragma: no cover
