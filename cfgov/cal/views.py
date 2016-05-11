from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from rest_framework import generics

from django.shortcuts import render, render_to_response
from django import forms
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cal.calendar_utils import tz_convert, EventCalendar
from cal.models import CFPBCalendar, CFPBCalendarEvent


class CalendarFilterForm(forms.Form):
   filter_calendar = forms.CharField(max_length=100)

   def clean_filter_calendar(self):
       import pdb;pdb.set_trace()

class PaginatorForSheerTemplates(Paginator):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PaginatorForSheerTemplates, self).__init__(*args, **kwargs)

    @property
    def pages(self):
        return self.num_pages

    def url_for_page(self,pagenum):
        url_args = self.request.GET.copy()
        url_args['page'] = pagenum
        return self.request.path +'?' + url_args.urlencode()

def display_html(request):
    """
    display (potentially filtered) html view of the calendar
    """

    form = CalendarFilterForm(request.GET)

    filtered_events = CFPBCalendarEvent.objects.filter(active=True)\
        .order_by('-dtstart')

    if form.is_valid():
        import pdb;pdb.set_trace()

    # largely ripped from the example
    paginator = PaginatorForSheerTemplates(request, filtered_events, 20)

    page = int(request.GET.get('page', 1))

    try:
        events = paginator.page(page)
	paginator.current_page = page
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
	paginator.current_page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
	paginator.current_page = paginator.num_pages

    context = {'events':events, 'paginator':paginator}

    return render(request, 'about-us/the-bureau/leadership-calendar/index.html',
       context )
