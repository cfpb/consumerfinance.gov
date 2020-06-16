from wagtail.core import hooks

from research_reports.models import Report


def process_research_report(request, page):
    if page.specific_class == Report:
        page.parse_report_file()


hooks.register('after_create_page', process_research_report)
hooks.register('after_edit_page', process_research_report)
