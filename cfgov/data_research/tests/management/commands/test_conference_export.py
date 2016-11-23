from django.test import TestCase
from model_mommy import mommy
from wagtail.wagtailcore.models import Page

from data_research.models import ConferenceRegistration
from data_research.management.commands.conference_export import (
    ConferenceExporter, get_registration_form_from_page
)
from scripts import _atomic_helpers as atomic
from v1.models import BrowsePage
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.migrations import set_stream_data


class TestGetRegistrationFormFromPage(TestCase):
    def test_raises_if_no_form_block(self):
        page = BrowsePage(title='test', slug='test')
        revision = save_new_page(page)
        with self.assertRaises(RuntimeError):
            get_registration_form_from_page(revision.page_id)

    def test_returns_form_block(self):
        page = BrowsePage(title='test', slug='test')
        revision = save_new_page(page)
        registration_form_block = atomic.conference_registration_form
        set_stream_data(page, 'content', [registration_form_block])

        self.assertEqual(
            get_registration_form_from_page(revision.page_id),
            registration_form_block
        )


def make_page_with_form(code='TEST_CODE', capacity=999):
    page = BrowsePage(title='test', slug='test')
    revision = save_new_page(page)

    block = atomic.conference_registration_form.copy()
    block['value'].update({
        'code': code,
        'capacity': capacity,
    })

    set_stream_data(page, 'content', [block])
    return revision.page_id


class TestConferenceExporter(TestCase):
    def make_attendees(self, code, count):
        return mommy.make(ConferenceRegistration, code=code, _quantity=count)

    def test_no_page_raises_doesnotexist(self):
        with self.assertRaises(Page.DoesNotExist):
            ConferenceExporter(page_id=12345)

    def test_page_no_form_raises_runtimeerror(self):
        page = BrowsePage(title='empty', slug='empty')
        revision = save_new_page(page)

        with self.assertRaises(RuntimeError):
            ConferenceExporter(page_id=revision.page_id)

    def test_page_with_block_no_error(self):
        page_id = make_page_with_form()

        try:
            ConferenceExporter(page_id=page_id)
        except Exception:
            self.fail('valid page should not raise exception')

    def test_exporter_conference_code(self):
        page_id = make_page_with_form(code='foo')
        exporter = ConferenceExporter(page_id=page_id)
        self.assertEqual(exporter.conference_code, 'foo')

    def test_exporter_conference_capacity(self):
        page_id = make_page_with_form(capacity=314159)
        exporter = ConferenceExporter(page_id=page_id)
        self.assertEqual(exporter.conference_capacity, 314159)

    def test_exporter_not_at_capacity(self):
        page_id = make_page_with_form(code='FOO', capacity=100)
        self.make_attendees(code='FOO', count=99)
        exporter = ConferenceExporter(page_id=page_id)
        self.assertFalse(exporter.at_capacity)

    def test_exporter_at_capacity(self):
        page_id = make_page_with_form(code='FOO', capacity=100)
        self.make_attendees(code='FOO', count=100)
        exporter = ConferenceExporter(page_id=page_id)
        self.assertTrue(exporter.at_capacity)

    def test_exporter_attendees(self):
        page_id = make_page_with_form(code='FOO')
        self.make_attendees(code='FOO', count=50)
        self.make_attendees(code='BAR', count=50)
        exporter = ConferenceExporter(page_id=page_id)
        self.assertEqual(exporter.count, 50)
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
            'Morning,Afternoon'
        )

    def test_prepare_field_to_row_no_sessions(self):
        attendee = mommy.prepare(ConferenceRegistration, sessions='')
        self.assertEqual(
            ConferenceExporter.prepare_field(attendee, 'sessions'),
            ''
        )

    def test_email_message_subject_not_at_capacity(self):
        page_id = make_page_with_form()
        exporter = ConferenceExporter(page_id=page_id)
        message = exporter.create_email_message('from', ['to'])
        self.assertIn('Update', message.subject)

    def test_email_message_subject_at_capacity(self):
        page_id = make_page_with_form(capacity=0)
        exporter = ConferenceExporter(page_id=page_id)
        message = exporter.create_email_message('from', ['to'])
        self.assertIn('Full', message.subject)


class TestExporterWithFixture(TestCase):
    fixtures = ['conference_export.json']

    def test_fixture_load(self):
        self.assertEqual(ConferenceRegistration.objects.count(), 4)

    def test_csv(self):
        page_id = make_page_with_form(code='CODE')
        exporter = ConferenceExporter(page_id=page_id)
        csv = exporter.to_csv()
        self.assertEqual(len(csv.strip().split('\n')), 4)

    def test_email_message(self):
        page_id = make_page_with_form(code='CODE')
        exporter = ConferenceExporter(page_id=page_id)
        message = exporter.create_email_message('from', ['to'])
        self.assertEqual(message.from_email, 'from')
        self.assertEqual(message.to, ['to'])
        self.assertEqual(len(message.attachments), 1)
