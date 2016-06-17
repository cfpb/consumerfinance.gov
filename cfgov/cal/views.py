import sys
import os
import six
import urllib2
from httplib import BadStatusLine

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from rest_framework import generics

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django import forms
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min

from cal.calendar_utils import tz_convert, EventCalendar
from cal.models import CFPBCalendar, CFPBCalendarEvent


## TODO: Update to python 3 when PDFreactor's python wrapper supports it.
if six.PY2:
    try:
        sys.path.append(os.environ.get('PDFREACTOR_LIB'))
        from PDFreactor import *
    except ImportError:
       PDFreactor = None


class CalendarFilterForm(forms.Form):
    filter_calendar = forms.MultipleChoiceField(
            choices = [(c.title, c.title) for c in CFPBCalendar.objects.all()],
            required=False)
    filter_range_date_gte = forms.DateField(required=False)
    filter_range_date_lte = forms.DateField(required=False)

    def clean_filter_calendar(self):
        calendar_names = self.cleaned_data['filter_calendar']
        calendars = CFPBCalendar.objects.filter(title__in=calendar_names)
        return calendars


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


def display(request, pdf=False):
    """
    display (potentially filtered) html view of the calendar
    """

    form = CalendarFilterForm(request.GET)

    filtered_events = CFPBCalendarEvent.objects.filter(active=True)\
        .order_by('-dtstart')

    if form.is_valid():
        if form.cleaned_data.get('filter_calendar', None):
            calendars = form.cleaned_data['filter_calendar']

            filtered_events = filtered_events.filter(calendar__in=calendars)

        if form.cleaned_data.get('filter_range_date_gte'):
            gte = form.cleaned_data['filter_range_date_gte']
            filtered_events = filtered_events.filter(dtstart__gte=gte)

        if form.cleaned_data.get('filter_range_date_lte'):
            # adding timedelta(days=1) makes the end of the range inclusive
            lte = form.cleaned_data['filter_range_date_lte']+ timedelta(days=1)
            filtered_events = filtered_events.filter(dtend__lte=lte)
    else:
        import pdb;pdb.set_trace()
    paginator = PaginatorForSheerTemplates(request, filtered_events, 20)

    page = int(request.GET.get('page', 1))

    if pdf:
        events = filtered_events
        template_name = 'about-us/the-bureau/leadership-calendar/print/index.html'
        paginator = None
    else:
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
        template_name='about-us/the-bureau/leadership-calendar/index.html'

    stats = filtered_events.aggregate(Min('dtstart'), Max('dtend'))
    range_start = form.cleaned_data.get('filter_range_date_gte') or stats['dtstart__min']
    range_end = form.cleaned_data.get('filter_range_date_lte') or stats['dtend__max']

    context = {'events':events, 'paginator':paginator,
            'form':form, 'range_start': range_start, 'range_end':range_end}

    if pdf and PDFreactor:
        license = os.environ.get('PDFREACTOR_LICENSE')
        stylesheet_url = 'http://localhost/static/css/pdfreactor-fonts.css'
        pdf_reactor = PDFreactor()

        pdf_reactor.setLogLevel(PDFreactor.LOG_LEVEL_WARN)
        pdf_reactor.setLicenseKey(str(license))
        pdf_reactor.setAuthor('CFPB')
        pdf_reactor.setAddTags(True)
        pdf_reactor.setAddBookmarks(True)
        pdf_reactor.addUserStyleSheet('', '', '', stylesheet_url)

        template = get_template(template_name)
        html = template.render(context)
        html = html.replace(u"\u2018", "'").replace(u"\u2019", "'")
        try:
            pdf = pdf_reactor.renderDocumentFromContent(html.encode('utf-8'))
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=cfpb-leadership.pdf'
            return response
        except (urllib2.HTTPError, urllib2.URLError, BadStatusLine):
            pass


    return render(request, template_name,
       context )
