from datetime import timedelta
from v1.models.learn_page import EventPage, AgendaItemBlock
from pytz import timezone

# We have been storing dates selected from the Datepicker as UTC, 
# without first telling the system the date was in ET at selection.
# This will be fixed going forward, but we need to update the
# existing datetimes in the database to be correct. Adding 4 hours
# to the datetime solves this because that is what ET -> UTC would
# look like. 
def run():

    # Update EventPages
    for e in EventPage.objects.all().filter(start_dt__isnull=False):
        previous_dt = e.start_dt
        e.start_dt = e.start_dt.replace(tzinfo=None)
        e.start_dt = timezone('US/Eastern').localize(e.start_dt)
        e.start_dt = e.start_dt.astimezone(timezone('UTC'))
        e.save()
        print "Updated start_dt for EventPage '%s' from %s to %s " %(e.title, previous_dt, e.start_dt)

    for e in EventPage.objects.all().filter(end_dt__isnull=False):
        previous_dt = e.end_dt
        e.end_dt = e.end_dt.replace(tzinfo=None)
        e.end_dt = timezone('US/Eastern').localize(e.end_dt)
        e.end_dt = e.end_dt.astimezone(timezone('UTC'))
        e.save()
        print "Updated end_dt for EventPage '%s' from %s to %s " %(e.title, previous_dt, e.end_dt)

    for e in EventPage.objects.all().filter(live_stream_date__isnull=False):
        previous_dt = e.live_stream_date
        e.live_stream_date = e.live_stream_date.replace(tzinfo=None)
        e.live_stream_date = timezone('US/Eastern').localize(e.live_stream_date)
        e.live_stream_date = e.live_stream_date.astimezone(timezone('UTC'))
        e.save()
        print "Updated live_stream_date for EventPage '%s' from %s to %s " %(e.title, previous_dt, e.live_stream_date)

    for e in EventPage.objects.all():
        for a in e.agenda_items:
            if a.value['start_dt']:
                previous_dt = a.value['start_dt']
                a.value['start_dt'] = a.value['start_dt'].replace(tzinfo=None)
                a.value['start_dt'] = timezone('US/Eastern').localize(a.value['start_dt'])
                a.value['start_dt'] = a.value['start_dt'].astimezone(timezone('UTC'))
                print "Updated start_dt for Agenda Item '%s' from %s to %s " %(a.value['description'], previous_dt, a.value['start_dt'])
            if a.value['end_dt']:
                previous_dt = a.value['end_dt']
                a.value['end_dt'] = a.value['end_dt'].replace(tzinfo=None)
                a.value['end_dt'] = timezone('US/Eastern').localize(a.value['end_dt'])
                a.value['end_dt'] = a.value['end_dt'].astimezone(timezone('UTC'))
                print "Updated end_dt for Agenda Item '%s' from %s to %s " %(a.value['description'], previous_dt, a.value['end_dt'])
        e.save()
        revision = e.save_revision()
        revision.publish()


