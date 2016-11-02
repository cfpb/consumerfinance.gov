import mock
import urllib2

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from mock import MagicMock, Mock, patch

from cal.views import (
    display, get_calendar_events_query, pdf_response, set_cal_events_context,
    set_pagination_context
)


class TestCalendarEvents(TestCase):
    def setUp(self):
        self.url = reverse('the-bureau:leadership-calendar')
        self.hash = '#leadership-pdf-calendar'
        self.request = RequestFactory().get(self.url)

        self.context = {
            'request': self.request,
            'form': MagicMock(),
        }

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarFilterForm')
    def test_display_calls_form_is_valid(self, mock_form_class, mock_render):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = False
        mock_form_class.return_value = mock_form
        display(self.request)
        assert mock_form.is_valid.called

    @mock.patch('cal.views.PDFreactor')
    @mock.patch('cal.views.pdf_response')
    @mock.patch('cal.views.CalendarPDFForm')
    @mock.patch('cal.views.set_cal_events_context')
    def test_display_calls_pdf_response(self, context, form, pdf_response,
                                        pdfreactor):
        display(self.request, pdf=True)
        self.assertEqual(pdf_response.call_count, 1)

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarPDFForm')
    @mock.patch('cal.views.set_cal_events_context')
    def test_display_calls_render_if_no_pdfreactor(
            self, context, form, render):
        display(self.request, pdf=True)
        self.assertEqual(render.call_count, 1)
        self.assertEqual(
            render.call_args[0][0:2],
            (
                self.request,
                'about-us/the-bureau/leadership-calendar/print/index.html',
            )
        )

    @mock.patch('cal.views.render')
    @mock.patch('cal.views.CalendarFilterForm')
    @mock.patch('cal.views.set_pagination_context')
    @mock.patch('cal.views.set_cal_events_context')
    def test_display_calls_set_pagination_context(
            self, mock_set_cal_events_context, mock_set_pagination_context,
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
    def test_display_calls_render_for_regular_view(
            self, mock_set_cal_events_context, mock_set_pagination_context,
            mock_form_class, mock_render):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form_class.return_value = mock_form
        template_name = 'about-us/the-bureau/leadership-calendar/index.html'
        display(self.request)
        assert mock_render.called
        mock_render.assert_called_with(self.request,
                                       template_name,
                                       {'form': mock_form})


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
    def test_calls_configure_page_days(
            self, mock_configure_page_days, mock_paginator):
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
        self.url = reverse('the-bureau:leadership-calendar')
        self.hash = '#leadership-pdf-calendar'
        self.request = RequestFactory().get(self.url)

        self.context = {
            'request': self.request,
            'form': MagicMock(),
        }

    @mock.patch('cal.views.PDFreactor')
    def test_returns_http_response(self, pdfreactor):
        response = pdf_response(self.request, self.context)
        self.assertIsInstance(response, HttpResponse)

    @mock.patch('cal.views.PDFreactor')
    def test_returns_file(self, pdfreactor):
        response = pdf_response(self.request, self.context)
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename=cfpb-leadership.pdf'
        )

    @patch('cal.views.messages')
    @patch('cal.views.PDFreactor', return_value=Mock(
        renderDocumentFromContent=Mock(side_effect=urllib2.URLError(1))
    ))
    def test_pdfreactor_error_sets_message(self, pdfreactor, messages):
        pdf_response(self.request, self.context)
        self.assertEqual(messages.error.call_count, 1)

    @patch('cal.views.messages')
    @patch('cal.views.PDFreactor', return_value=Mock(
        renderDocumentFromContent=Mock(side_effect=urllib2.URLError(1))
    ))
    def test_pdfreactor_error_redirects(self, pdfreactor, messages):
        response = pdf_response(self.request, self.context)
        self.assertEqual(
            (response['Location'], response.status_code),
            (self.url + self.hash, 302)
        )
