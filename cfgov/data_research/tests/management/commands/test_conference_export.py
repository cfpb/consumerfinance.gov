from django.test import TestCase
from model_mommy import mommy
from wagtail.wagtailcore.models import Page

from data_research.models import ConferenceRegistration
from data_research.management.commands.conference_export import (
    ConferenceExporter, get_registration_form_from_slug
)
from scripts import _atomic_helpers as atomic
from v1.models import BrowsePage
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import set_stream_data


class TestGetRegistrationFormFromSlug(TestCase):
    def test_raises_if_no_form_block(self):
        page = BrowsePage(title='test', slug='test')
        save_new_page(page)
        with self.assertRaises(RuntimeError):
            get_registration_form_from_slug('test')

    def test_returns_form_block(self):
        page = BrowsePage(title='test', slug='test')
        save_new_page(page)
        registration_form_block = atomic.conference_registration_form
        set_stream_data(page, 'content', [registration_form_block])

        self.assertEqual(
            get_registration_form_from_slug('test'),
            registration_form_block
        )


def make_page_with_form(slug, code='TEST_CODE', capacity=999):
    page = BrowsePage(title='test', slug=slug)
    save_new_page(page)

    block = atomic.conference_registration_form.copy()
    block['value'].update({
        'code': code,
        'capacity': capacity,
    })

    set_stream_data(page, 'content', [block])


class TestConferenceExporter(TestCase):
    def make_attendees(self, code, count):
        return mommy.make(ConferenceRegistration, code=code, _quantity=count)

    def test_no_page_raises_doesnotexist(self):
        with self.assertRaises(Page.DoesNotExist):
            ConferenceExporter(page_slug='missing')

    def test_page_no_form_raises_runtimeerror(self):
        page = BrowsePage(title='empty', slug='empty')
        save_new_page(page)

        with self.assertRaises(RuntimeError):
            ConferenceExporter(page_slug='empty')

    def test_page_with_block_no_error(self):
        make_page_with_form(slug='test')

        try:
            ConferenceExporter(page_slug='test')
        except Exception:
            self.fail('valid page should not raise exception')

    def test_exporter_conference_code(self):
        make_page_with_form(slug='test', code='foo')
        exporter = ConferenceExporter(page_slug='test')
        self.assertEqual(exporter.conference_code, 'foo')

    def test_exporter_conference_capacity(self):
        make_page_with_form(slug='test', capacity=314159)
        exporter = ConferenceExporter(page_slug='test')
        self.assertEqual(exporter.conference_capacity, 314159)

    def test_exporter_not_at_capacity(self):
        make_page_with_form(slug='test', code='FOO', capacity=100)
        self.make_attendees(code='FOO', count=99)
        exporter = ConferenceExporter(page_slug='test')
        self.assertFalse(exporter.at_capacity)

    def test_exporter_at_capacity(self):
        make_page_with_form(slug='test', code='FOO', capacity=100)
        self.make_attendees(code='FOO', count=100)
        exporter = ConferenceExporter(page_slug='test')
        self.assertTrue(exporter.at_capacity)

    def test_exporter_attendees(self):
        make_page_with_form(slug='test', code='FOO')
        self.make_attendees(code='FOO', count=50)
        self.make_attendees(code='BAR', count=50)
        exporter = ConferenceExporter(page_slug='test')
        self.assertEqual(exporter.attendees.count(), 50)
        self.assertEqual(exporter.attendees.first().code, 'FOO')

    def test_prepare_field_to_row_unicode(self):
        attendee = mommy.prepare(
            ConferenceRegistration,
            organization=u'Citro\xebn'
        )
        self.assertEqual(
            ConferenceExporter.prepare_field(attendee, 'organization'),
            'Citro\xc3\xabn'
        )

    def test_prepare_field_to_row_sessions(self):
        attendee = mommy.prepare(
            ConferenceRegistration,
            sessions='["Morning", "Afternoon"]'
        )
        self.assertEqual(
            ConferenceExporter.prepare_field(attendee, 'sessions'),
            'Morning, Afternoon'
        )

    def test_prepare_field_to_row_no_sessions(self):
        attendee = mommy.prepare(ConferenceRegistration, sessions='')
        self.assertEqual(
            ConferenceExporter.prepare_field(attendee, 'sessions'),
            ''
        )

    def test_email_message_subject_not_at_capacity(self):
        make_page_with_form(slug='test')
        exporter = ConferenceExporter(page_slug='test')
        message = exporter.create_email_message('from', ['to'])
        self.assertIn('Update', message.subject)

    def test_email_message_subject_at_capacity(self):
        make_page_with_form(slug='test', capacity=0)
        exporter = ConferenceExporter(page_slug='test')
        message = exporter.create_email_message('from', ['to'])
        self.assertIn('Full', message.subject)


class TestExporterWithFixture(TestCase):
    fixtures = ['conference_export.json']

    def test_fixture_load(self):
        self.assertEqual(ConferenceRegistration.objects.count(), 4)

    def test_csv(self):
        make_page_with_form(slug='test', code='CODE')
        exporter = ConferenceExporter(page_slug='test')
        csv = exporter.to_csv()
        self.assertEqual(len(csv.strip().split('\n')), 4)

    def test_email_message(self):
        make_page_with_form(slug='test', code='CODE')
        exporter = ConferenceExporter(page_slug='test')
        message = exporter.create_email_message('from', ['to'])
        self.assertEqual(message.from_email, 'from')
        self.assertEqual(message.to, ['to'])
        self.assertEqual(len(message.attachments), 1)
