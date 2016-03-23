from datetime import timedelta
from v1.models.learn_page import EventPage, AgendaItemBlock

# We have been storing dates selected from the Datepicker as UTC, 
# without first telling the system the date was in ET at selection.
# This will be fixed going forward, but we need to update the
# existing datetimes in the database to be correct. Adding 4 hours
# to the datetime solves this because that is what ET -> UTC would
# look like. 
def run():

    # Update EventPages
    for e in EventPage.objects.all().filter(start_dt__isnull=False):
        e.start_dt += timedelta(hours=4)
        e.save()

    for e in EventPage.objects.all().filter(end_dt__isnull=False):
        e.end_dt += timedelta(hours=4)
        e.save()

    for e in EventPage.objects.all().filter(live_stream_date__isnull=False):
        e.live_stream_date += timedelta(hours=4)
        e.save()

    for e in EventPage.objects.all():
        for a in e.agenda_items:
            if a.value['start_dt']:
                a.value['start_dt'] += timedelta(hours=4)
            if a.value['end_dt']:
                a.value['end_dt'] += timedelta(hours =4)
        e.save()


