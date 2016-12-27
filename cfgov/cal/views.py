import os
import sys
import urllib2
from datetime import timedelta
from httplib import BadStatusLine

import six
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.db.models import Max, Min, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template

from cal.forms import CalendarFilterForm, CalendarPDFForm
from cal.models import CFPBCalendarEvent

# TODO: Update to python 3 when PDFreactor's python wrapper supports it.
if six.PY2:
    try:
        sys.path.append(os.environ.get('PDFREACTOR_LIB'))
        from PDFreactor import PDFreactor
    except ImportError:
        PDFreactor = None


class PaginatorForSheerTemplates(Paginator):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PaginatorForSheerTemplates, self).__init__(*args, **kwargs)

    @property
    def pages(self):
        return self.num_pages

    def url_for_page(self, pagenum):
        url_args = self.request.GET.copy()
        url_args['page'] = pagenum
        return self.request.path + '?' + url_args.urlencode()


def display(request, pdf=False):
    """
    display (potentially filtered) html view of the calendar
    """

    template_name = 'about-us/the-bureau/leadership-calendar/index.html'
    form = (CalendarPDFForm(request.GET) if pdf
            else CalendarFilterForm(request.GET))
    context = {'form': form}
    form_is_valid = form.is_valid()

    if form.is_valid():
        set_cal_events_context(context)

        if pdf:
            template_name = \
                'about-us/the-bureau/leadership-calendar/print/index.html'
            if PDFreactor:
                return pdf_response(request, context)
            else:
                return render(request, template_name, context)

        set_pagination_context(request, context)

    elif not form_is_valid and pdf:
        for error in form.errors.itervalues():
            messages.error(request,
                           u''.join(error).encode('utf-8', errors='ignore'),
                           extra_tags='leadership-calendar')
        return redirect_to_leadership_view()

    return render(request, template_name, context)


def set_cal_events_context(context):
    cal_q = get_calendar_events_query(context['form'])
    events = CFPBCalendarEvent.objects.filter(cal_q).order_by('-dtstart')
    stats = events.aggregate(Min('dtstart'), Max('dtend'))
    range_start = (context['form'].cleaned_data.get('filter_range_date_gte')
                   or stats['dtstart__min'])
    range_end = (context['form'].cleaned_data.get('filter_range_date_lte')
                 or stats['dtend__max'])

    context.update({
        'events': events,
        'range_start': range_start,
        'range_end': range_end,
    })


def get_calendar_events_query(form):
    cal_q = Q(('active', True))
    if form.cleaned_data.get('filter_calendar', None):
        calendars = form.cleaned_data['filter_calendar']
        cal_q &= Q(('calendar__in', calendars))

    if form.cleaned_data.get('filter_range_date_gte'):
        gte = form.cleaned_data['filter_range_date_gte']
        cal_q &= Q(('dtstart__gte', gte))

    if form.cleaned_data.get('filter_range_date_lte'):
        # adding timedelta(days=1) makes the end of the range inclusive
        lte = form.cleaned_data['filter_range_date_lte'] + timedelta(days=1)
        cal_q &= Q(('dtend__lte', lte))

    return cal_q


def set_pagination_context(request, context):
    datetimes = context['events'].datetimes('dtstart', 'day', order='DESC')
    paginator = PaginatorForSheerTemplates(request, datetimes, 5)
    page_num = int(request.GET.get('page', 1))

    try:
        page_days = paginator.page(page_num)
        paginator.current_page = page_num
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_days = paginator.page(1)
        paginator.current_page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_days = paginator.page(paginator.num_pages)
        paginator.current_page = paginator.num_pages

    configure_page_days(page_days)

    context.update({
        'paginator': paginator,
        'page_days': page_days,
    })


def configure_page_days(page_days):
    # The first date in the list needs to include all the events for that day
    days = list(page_days.object_list)
    if days:
        if len(days) == 1:
            # If there's only one day of events then duplicate it
            days = [days[0], days[0]]
        days[0] += timedelta(hours=23, minutes=59, seconds=59)
        page_days.object_list = days


def pdf_response(request, context):
    template_name = 'about-us/the-bureau/leadership-calendar/print/index.html'
    license = os.environ.get('PDFREACTOR_LICENSE')
    stylesheet_url = '/static/css/pdfreactor-fonts.css'
    pdf_reactor = PDFreactor()

    pdf_reactor.setBaseURL("http://localhost/")
    pdf_reactor.setLogLevel(PDFreactor.LOG_LEVEL_FATAL)
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
        response['Content-Disposition'] = \
            'attachment; filename=cfpb-leadership.pdf'
        return response
    except (urllib2.HTTPError, urllib2.URLError, BadStatusLine):
        messages.error(request,
                       'Error Creating PDF',
                       extra_tags='leadership-calendar')
        return redirect_to_leadership_view()


def redirect_to_leadership_view():
    view_name = 'the-bureau:leadership-calendar'
    anchor_hash = '#leadership-pdf-calendar'
    return HttpResponseRedirect(reverse(view_name) + anchor_hash)
