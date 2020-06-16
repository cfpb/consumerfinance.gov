from django.core.management.base import BaseCommand
from research_reports.models import Report
import pypandoc


def run(report_page):
    print(" *** downloading the report file... ***")
    with report_page.report_file.file.file.open() as f:
        raw_report = f.read()

    print(" *** converting the report with pandoc... ***")
    output = pypandoc.convert_text(raw_report, format='docx', to='html')

    print(" *** updating a field... ***")
    report_page.footnotes = output

    print(" *** saving the page... ***")
    report_page.process_report = False
    report_page.save_revision()  # future: add user= keyword
    report_page.save()


# Invoke this script from the cfgov-refresh root with this command:
#     cfgov/manage.py build_test [report_page_id]
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('report_page_id', type=int)

    def handle(self, *args, **options):
        report_id = options['report_page_id']
        print('received id as argument: ', id)

        print(" *** finding report page... ***")
        report_page = Report.objects.get(id=report_id)
        run(report_page)
