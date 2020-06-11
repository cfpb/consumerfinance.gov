from django.core.management.base import BaseCommand
from v1.models.learn_page import EventPage


def run(report_id):
    print(" *** finding report page... ***")
    mp = EventPage.objects.get(id=report_id)
    print(" *** updating a static field... ***")
    mp.body = 'here is more content'
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
