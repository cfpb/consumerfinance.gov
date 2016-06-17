from cal.models import CFPBCalendar, CFPBCalendarEvent, CFPBImportICSFile
from cal import event
from datetime import datetime
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from event import ProcessEvent
from icalendar import Calendar
import sys


def activate(modeladmin, request, queryset):
    queryset.update(active=True)
activate.short_description = "Mark selected events as active"

def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)
deactivate.short_description = "Mark selected events as inactive"

class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['active', 'start_date', 'summary', 'description', 'location']
    list_display_links = ['active', 'start_date', 'summary']

    ordering = ['-dtstart']
    actions = [activate, deactivate]

    def start_date(self, obj):
        return obj.dtstart
    start_date.short_description = 'Start Date'

class CFPBPDFFileAdmin(admin.ModelAdmin):
    ordering = ['-id']

class CFPBCalendarImportICSFileAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        context = {}
        context.update(extra_context or {})
        context.update({ 'icsfile': None,})
        context.update({ 'calendar_record': None,})
        context.update({ 'processed_events': None,})

        leadership = CFPBCalendar.objects.all().order_by("title")

        context.update({ 'leadership': leadership,})
        error = []

        if request.method == 'POST':
            icsfile = request.FILES['icsfile']

            if icsfile:
                file_type = icsfile.content_type.split('/')[0]

                if(file_type != "text"):
                    error.append( (['There was an error with the File'],["Incorrect File Type"]) )
                    context.update({ 'error': error,})
                    return super(CFPBCalendarImportICSFileAdmin,self).changelist_view(request,context)

            try:

                file_content = icsfile.read()

                ical_events = Calendar.from_ical(file_content)

            except:
                e = sys.exc_info()
                error.append( (['There was an error with the File'],e) )
                context.update({ 'error': error,})
                return super(CFPBCalendarImportICSFileAdmin,self).changelist_view(request,context)

            leader_id = request.POST['drpLeader']

            calendar_record = CFPBCalendar.objects.get(pk=int(leader_id))

            context.update({ 'calendar_record': calendar_record,})

            processed_events = []

            for event in ical_events.walk('vevent'):
                try:
                    pe = ProcessEvent(event, calendar_record)
                    pe.save()
                    processed_events.append(pe)
                except:
                    e = sys.exc_info()
                    error.append( (event,e) )

            processed_events.sort(key=lambda x: x.e.dtstart, reverse=True)
            context.update({ 'processed_events': processed_events,})

        context.update({ 'error': error,})

        return super(CFPBCalendarImportICSFileAdmin,self).changelist_view(request,context)


admin.site.register(CFPBCalendar, admin.ModelAdmin)
admin.site.register(CFPBCalendarEvent, CalendarEventAdmin)
admin.site.register(CFPBImportICSFile, CFPBCalendarImportICSFileAdmin)
