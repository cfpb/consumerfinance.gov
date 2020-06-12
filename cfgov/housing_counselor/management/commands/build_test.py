from django.core.management.base import BaseCommand
from v1.models.learn_page import EventPage
import pypandoc


def run(report_id):
    print(" *** finding report page... ***")
    mp = EventPage.objects.get(id=report_id)

    print(" *** downloading the report file... ***")
    with mp.speech_transcript.file.file.open() as f:
        raw_report = f.read()

    print(" *** converting the report with pandoc... ***")
    output = pypandoc.convert_text(raw_report, 'docx', format='html')

    print(" *** updating body field... ***")
    mp.body = output

    print(" *** saving the page... ***")
    mpr = mp.save_revision()  # future: add user= keyword
    mp.save()


# Invoke this script from the cfgov-refresh root with this command:
#     cfgov/manage.py build_test [report_page_id]
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('report_page_id', type=int)

    def handle(self, *args, **options):
        id = options['report_page_id']
        print('received report id as positional argument: ', id)
        run(id) # for testing on build today, id should be 41955
