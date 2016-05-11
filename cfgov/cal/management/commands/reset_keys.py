from django.core.management.base import NoArgsCommand
from cal.models import CFPBCalendar, CFPBCalendarEvent
import uuid

class Command(NoArgsCommand):
    help = "replace each calendar entry with a unique identifier"
    
    def handle_noargs(self, **options):
            
        calendar_record = CFPBCalendar.objects.get(slug='professor_warren') 
        events = CFPBCalendarEvent.objects.filter(calendar=calendar_record)

        for event in events:
            event.uid = uuid.uuid4()
            event.save()