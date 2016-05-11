from cal.models import CFPBCalendar, CFPBCalendarEvent
from datetime import date, datetime

class ProcessEvent(object):

    # pass in an icalendar event and the calendar table that was queried
    def __init__(self, event ,calendar_record):
        self.event = event

        self.e = CFPBCalendarEvent()

        self.e.calendar = calendar_record

        self.num_dupes = 0

        self.saved_event = False

        self._process()

    # get rid of unicode and formatting issues
    def _clean_string(self,s):

        s = s.encode('ascii', 'ignore')
        s = str(s).replace('\\n', '').replace('\\,', ',')

        return s

    # convert the datetime to string and remove any timezone info
    def _clean_date(self,d):

        d = str(d).replace('Z', '')
        d = d.encode('ascii', 'ignore')
        d = d.split("+")[0]

        return d

    # figure out if this event is assigned for all day
    def _is_all_day(self):

        start = datetime.strptime(self.e.dtstart.split(" ")[0], "%Y-%m-%d")
        end =  datetime.strptime(self.e.dtend.split(" ")[0], "%Y-%m-%d")

        diff = start - end

        all_day = (diff.days == -1)

        setattr(self.e, "all_day", all_day)

    # dynamically set the value of the calendar object from the event data
    def _set_value(self, i):

        if i in ('DTSTART', 'DTEND', 'DTSTAMP', 'CREATED'):
            v = self._clean_date( self.event.decoded(i) )

        elif i in ('DESCRIPTION', 'SUMMARY', 'LOCATION'):
            v = self._clean_string(self.event[i])

        else:
            v = self.event[i]

        setattr(self.e, i.lower(), v)

    # make sure uid is unqiue - this is do to recurring events sharing the same uid
    def _create_unique_id(self):

        temp = str(self.e.uid)+'@'+str(self.e.dtstart).replace(" ","").replace(":","").replace("-","")

        self.e.uid=temp

    # let the magic happen
    def _process(self):

        for i in self.event.keys():
            self._set_value(i)

        if self.e.summary == None:
            summary_fill = CFPBCalendarEvent.objects.filter(uid__contains=self.e.uid )  #uid=self.e.uid, summary__isnull=False)

            if summary_fill:
                self.e.summary = summary_fill[0].summary

        if self.e.dtstamp == None:
             self.e.dtstamp = self._clean_date(self.event.decoded("RECURRENCE-ID"))

        if self.e.location == None:
            self.e.location = " "

        self._is_all_day()

        self._create_unique_id()

        dupes = CFPBCalendarEvent.objects.filter(uid=self.e.uid, dtstamp=self.e.dtstamp)

        self.num_dupes = len(dupes)

    def save(self):
        if self.num_dupes == 0:
            self.e.save()
            self.saved_event = True