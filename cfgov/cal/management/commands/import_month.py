from django.conf import settings
from django.core.management.base import  BaseCommand
from cal.models import CFPBCalendar, CFPBCalendarEvent
from icalendar import Calendar
from cal.event import ProcessEvent



class Command(BaseCommand):
    help = "import monthly .ics file"

    def handle(self, cal_id, ical_path, **options):
        calendar_record = CFPBCalendar.objects.get(pk=int(cal_id)) # pk=3 for Raj Date's calendar

        this_month = Calendar.from_ical(open(ical_path,'rb').read())

        counter = 0
        countersaved = 0

        for event in this_month.walk('vevent'):
            print "Processing Event for " + calendar_record.title
            pe = ProcessEvent(event, calendar_record)
            pe.save()
            print "Time Start: " + pe.e.dtstart
            print "Summary: " + str(pe.e.summary)
            print "Dupes Count:" + str(pe.num_dupes)
            print "DB Saved: " + str(pe.saved_event)

            if pe.saved_event:
                countersaved = countersaved + 1

            counter = counter + 1

            print "         "


        print "             "
        print "Total Events Read: " + str(counter)
        print "Total Events Saved: " + str(countersaved)


