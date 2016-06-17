import os
import sys

import six
import requests
import icalendar

from django.views.generic.base import View, ContextMixin
from django.http import HttpResponse, Http404
from django.core.exceptions import ImproperlyConfigured
from pytz import timezone
from dateutil.parser import parse
from v1.forms import CalenderPDFFilterForm
from django.core.urlresolvers import reverse, resolve
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings

class PDFReactorNotConfigured(Exception):
    pass

## TODO: Update to python 3 when PDFreactor's python wrapper supports it.
if six.PY2:
    try:
        sys.path.append(os.environ.get('PDFREACTOR_LIB'))
        from PDFreactor import *
    except:
       PDFreactor = None

class PDFGeneratorView(View):
    render_url = None
    stylesheet_url = None
    filename = None
    license = os.environ.get('PDFREACTOR_LICENSE')

    def get_render_url(self):
        if self.render_url is None:
            raise ImproperlyConfigured(
                "PDFGeneratorView requires either a definition of "
                "'render_url' or an implementation of 'get_render_url()'")
        return self.render_url

    def get_stylesheet_url(self):
        if self.stylesheet_url is None:
            raise ImproperlyConfigured(
                "PDFGeneratorView requires either a definition of "
                "'stylesheet_url' or an implementation of 'get_stylesheet_url()'")
        return self.stylesheet_url

    def get_filename(self):
        if self.filename is None:
            raise ImproperlyConfigured(
                "PDFGeneratorView requires either a definition of "
                "'filename' or an implementation of 'get_filename()'")
        return self.filename

    def generate_pdf(self, query_opts):
        if self.license is None:
            raise Exception("PDFGeneratorView requires a license")

        if settings.DEBUG and PDFreactor is None:
            return HttpResponse("PDF Reactor is not configured, can not render %s" % self.get_render_url())

        try:
            pdf_reactor = PDFreactor()
        except:
            raise PDFReactorNotConfigured('PDFreactor python library path needs to be configured.')

        pdf_reactor.setLogLevel(PDFreactor.LOG_LEVEL_WARN)
        pdf_reactor.setLicenseKey(str(self.license))
        pdf_reactor.setAuthor('CFPB')
        pdf_reactor.setAddTags(True)
        pdf_reactor.setAddBookmarks(True)
        pdf_reactor.addUserStyleSheet('', '', '', self.get_stylesheet_url())
        url = '{0}?filter_calendar={1}&filter_range_date_gte={2}&filter_range_date_lte={3}'.format(
                self.get_render_url(),
                query_opts['filter_calendar'],
                query_opts['filter_range_date_gte'],
                query_opts['filter_range_date_lte'])

        result = pdf_reactor.renderDocumentFromURL(url)

        # Check if successful
        if result is None:
            # Not successful, return 500
            raise Exception('Error while rendering PDF: {}'.format(
                pdf_reactor.getError()))
        else:
            # Set the correct header for PDF output
            response = HttpResponse(result, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(
                self.get_filename())
            return response

    def post(self, request):
        index = request.POST.get('form-id')
        filter_calendar = index + 'filter_calendar'
        filter_range_date_gte = index + '-filter_range_date_gte'
        filter_range_date_lte = index + '-filter_range_date_lte'
        form = CalenderPDFFilterForm({
            'filter_calendar': request.POST.get(filter_calendar),
            'filter_range_date_gte': request.POST.get(filter_range_date_gte),
            'filter_range_date_lte': request.POST.get(filter_range_date_lte),
        })
        if form.is_valid():
            query_opts = {
                'filter_calendar': form.cleaned_data.get('filter_calendar'),
                'filter_range_date_gte':
                    form.cleaned_data.get('filter_range_date_gte'),
                'filter_range_date_lte':
                    form.cleaned_data.get('filter_range_date_lte'),
            }
            return self.generate_pdf(query_opts)
        else:
            for error in form.errors.itervalues():
                messages.error(request, str(error),
                               extra_tags='leadership-calendar')
            return HttpResponseRedirect('/the-bureau/leadership-calendar/')

class ICSView(ContextMixin, View):
    """
    Returns an .ics file for a given calendar event
    """
    # Contants
    event_calendar_prodid = '-//CFPB//Calendar Item//EN',
    event_source = None

    # Default variables
    event_summary = ''
    event_dtstart = '2015-01-01T00:00:00'
    event_dtend = '2015-01-01T00:00:00'
    event_dtstamp = '2015-01-01T00:00:00'
    event_uid = ''
    event_priority = 1
    event_organizer = ''
    event_organizer_addr = ''
    event_location = ''
    event_status = 'TENTATIVE'

    def get_event_source(self):
        if self.event_source is None:
            raise ImproperlyConfigured(
                "ICSView requires an 'event_source' to be set.")
        return self.event_source

    def get_event_json(self, event_slug):
        source_template = self.get_event_source()
        source_url = source_template.replace('<event_slug>', event_slug)
        source_response = requests.get(source_url)
        try:
            self.event_json = source_response.json()['ics']
        except ValueError:
            self.event_json = {}
        return source_response.status_code

    def get_field_value(self, attribute):
        """
        Check if the attribute keyname was passed in; if so, get the value
        Otherwise, use the default attribute on this base class
        """
        attribute_variable = "{}_keyname".format(attribute)
        try:
            attribute_value = getattr(self, attribute_variable)
            return self.event_json.get(attribute_value, '')
        except AttributeError:
            attribute_value = getattr(self, attribute)
        return attribute_value

    def make_date_tz_aware(self, date, tzinfo_field):
        """
        Convert datetime-naive date to a datetime-aware date
        Specifically setting a location/TZ like this is required by icalendar
        """
        naive_date = parse(date)
        if self.event_json.get(tzinfo_field):
            tzname = self.event_json[tzinfo_field]
            aware_date = naive_date.astimezone(timezone(tzname))
        else:
            aware_date = timezone('UTC').localize(naive_date)
        return aware_date

    def generate_ics(self, event_slug):
        # Get the event json from our source
        source_status = self.get_event_json(event_slug)
        if source_status != 200:
            return HttpResponse('', status=source_status)

        # Create the Calendar
        calendar = icalendar.Calendar()
        calendar.add('prodid', self.event_calendar_prodid)
        calendar.add('version', '2.0')
        calendar.add('method', 'publish')

        # Create the event
        event = icalendar.Event()

         # Populate the event
        event.add('summary', self.get_field_value('event_summary'))
        event.add('uid', self.get_field_value('event_uid'))
        event.add('location', self.get_field_value('event_location'))
        dtstart = self.make_date_tz_aware(self.get_field_value('event_dtstart'),
                                          'starting_tzidnfo')
        dtend = self.make_date_tz_aware(self.get_field_value('event_dtend'),
                                        'ending_tzidnfo')
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        event.add('dtstamp', parse(self.get_field_value('event_dtstamp')))
        event.add('status', self.get_field_value('event_status'))

        # Create any persons associated with the event
        if self.get_field_value('event_organizer_addr') and \
                self.get_field_value('event_organizer'):
            organizer = icalendar.vCalAddress(
                'MAILTO:' + self.get_field_value('event_organizer_addr'))
            organizer.params['cn'] = icalendar.vText(
                self.get_field_value('event_organizer'))
            event.add('organizer', organizer)

        # Add the event to the calendar
        calendar.add_component(event)

        # Return the ICS formatted calendar
        response = HttpResponse(calendar.to_ical(),
                                content_type='text/calendar',
                                status=source_status,
                                charset='utf-8')
        response['Content-Disposition'] = 'attachment;filename={}.ics'.format(
            event_slug)
        return response

    def get(self, *args, **kwargs):
        event_slug = kwargs.get('doc_id')
        return self.generate_ics(event_slug) if event_slug else Http404
