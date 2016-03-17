import sys
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.sublanding_filterable_page import SublandingFilterablePage

def run(page_title):
    reports_page_exists = BrowseFilterablePage.objects.filter(title='Research and reports').exists()
    sublanding_filterable_page_exists = SublandingFilterablePage.objects.filter(title=page_title).exists()

    if sublanding_filterable_page_exists and reports_page_exists:
        reports = BrowseFilterablePage.objects.get(title='Research and reports')
        sublanding_pages = SublandingFilterablePage.objects.get(title=page_title)

        if len(reports.get_children()) >= 1:
            for child in reports.get_children():
                report = child.specific
                if report.can_move_to(sublanding_pages):
                    report.move(sublanding_pages, pos='last-child')
                    print report.title + ' Report .....archived'
        else:
            print 'No report to archive found....'
    elif not sublanding_filterable_page_exists:
        print 'Sublanding filterable page named \'%s\' has not been created....' %(page_title)
    elif not reports_page_exists:
        print 'No Browse filterable page named \'Research and reports\' exists....'

