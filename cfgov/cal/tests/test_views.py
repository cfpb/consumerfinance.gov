import mock
import json
import urllib2

from django.db.models import Q
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory

from cal.views import (
    display, get_calendar_events_query, pdf_response, set_cal_events_context,
    set_pagination_context
)


class TestCalendarEvents(TestCase):
    def setUp(self):
        self.request = mock.Mock()

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarFilterForm')
    def test_display_calls_form_is_valid(self, mock_form_class, mock_render):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = False
        mock_form_class.return_value = mock_form
        display(self.request)
        assert mock_form.is_valid.called

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarFilterForm')
    @mock.patch('cal.views.pdf_response')
    @mock.patch('cal.views.set_cal_events_context')
    @mock.patch('cal.views.PDFreactor')
    def test_display_calls_pdf_response(self, mock_PDFreactor,
            mock_set_cal_events_context, mock_pdf_response, mock_form_class,
            mock_render):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form_class.return_value = mock_form
        display(self.request, pdf=True)
        assert mock_set_cal_events_context.called
        assert mock_pdf_response.called

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarFilterForm')
    @mock.patch('cal.views.pdf_response')
    @mock.patch('cal.views.set_cal_events_context')
    def test_display_calls_render_for_print(self, mock_set_cal_events_context,
            mock_pdf_response, mock_form_class, mock_render):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form_class.return_value = mock_form
        template_name = 'about-us/the-bureau/leadership-calendar/print/index.html'
        display(self.request, pdf=True)
        mock_render.assert_called_with(self.request, template_name, {'form': mock_form})

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarFilterForm')
    @mock.patch('cal.views.set_pagination_context')
    @mock.patch('cal.views.set_cal_events_context')
    def test_display_calls_set_pagination_context(self,
            mock_set_cal_events_context, mock_set_pagination_context,
            mock_form_class, mock_render):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form_class.return_value = mock_form
        display(self.request)
        assert mock_set_pagination_context.called

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarFilterForm')
    @mock.patch('cal.views.set_pagination_context')
    @mock.patch('cal.views.set_cal_events_context')
    def test_display_calls_render_for_regular_view(self,
            mock_set_cal_events_context, mock_set_pagination_context,
            mock_form_class, mock_render):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form_class.return_value = mock_form
        template_name = 'about-us/the-bureau/leadership-calendar/index.html'
        display(self.request)
        assert mock_render.called
        mock_render.assert_called_with(self.request, template_name, {'form': mock_form})


class TestSetCalendarEventsContext(TestCase):
    @mock.patch('cal.views.PaginatorForSheerTemplates')
    def setUp(self, mock_paginator):
        self.form = mock.Mock()
        self.context = {'form': self.form}

    @mock.patch('cal.views.CFPBCalendarEvent')
    @mock.patch('cal.views.get_calendar_events_query')
    def test_calls_get_calendar_query(self, mock_query_fn, mock_event_class):
        set_cal_events_context(self.context)
        assert mock_query_fn.called

    @mock.patch('cal.views.CFPBCalendarEvent')
    @mock.patch('cal.views.get_calendar_events_query')
    def test_updates_context(self, mock_query_fn, mock_event_class):
        set_cal_events_context(self.context)
        for key in ['events', 'range_start', 'range_end', 'form']:
            assert key in self.context.keys()


class TestCalendarEventsQuery(TestCase):
    def setUp(self):
        self.form = mock.MagicMock()

    def test_returns_query(self):
        result = get_calendar_events_query(self.form)
        assert type(result) is Q


class TestSetPaginationContext(TestCase):
    def setUp(self):
        self.request = mock.Mock()
        self.request.GET.get.return_value = 1
        self.context = {'events': mock.Mock()}

    @mock.patch('cal.views.PaginatorForSheerTemplates')
    @mock.patch('cal.views.configure_page_days')
    def test_calls_configure_page_days(self, mock_configure_page_days,
            mock_paginator):
        set_pagination_context(self.request, self.context)
        assert mock_configure_page_days.called

    @mock.patch('cal.views.PaginatorForSheerTemplates')
    @mock.patch('cal.views.configure_page_days')
    def test_sets_context(self, mock_configure_page_days, mock_paginator):
        set_pagination_context(self.request, self.context)
        assert 'paginator' in self.context
        assert 'page_days' in self.context


class TestPDFResponse(TestCase):
    def setUp(self):
        self.request = mock.Mock()
        self.context = mock.Mock()

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.get_template')
    @mock.patch('cal.views.PDFreactor')
    def test_returns_http_response(self, mock_pdf_reactor, mock_get_template,
            mock_render):
        pdf_reactor = mock.MagicMock()
        result = pdf_response(self.request, self.context)
        assert type(result) is HttpResponse

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.HttpResponse')
    @mock.patch('cal.views.get_template')
    @mock.patch('cal.views.PDFreactor')
    def test_calls_render(self, mock_pdf_reactor, mock_get_template,
            mock_HttpResponse, mock_render):
        mock_HttpResponse.side_effect = urllib2.URLError(1)
        pdf_response(self.request, self.context)
        assert mock_render.called
