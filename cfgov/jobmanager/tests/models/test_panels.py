from django.core.exceptions import ValidationError
from django.test import TestCase

from wagtail.wagtailcore.models import Page

from mock import Mock
from model_mommy import mommy

from jobmanager.models.django import ApplicantType, JobLocation
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import (
    EmailApplicationLink, USAJobsApplicationLink
)


class ApplicationLinkTestCaseMixin(object):
    link_cls = None

    @classmethod
    def setUpClass(cls):
        super(ApplicationLinkTestCaseMixin, cls).setUpClass()
        cls.root = Page.objects.get(slug='root')

    def setUp(self):
        location = JobLocation.objects.create(abbreviation='US', name='USA')
        self.job_listing = mommy.prepare(
            JobListingPage,
            description='foo',
            location=location
        )
        self.job_listing.full_clean = Mock(return_value=None)
        self.root.add_child(instance=self.job_listing)

    def check_clean(self, **kwargs):
        link = self.link_cls(job_listing=self.job_listing, **kwargs)
        link.full_clean()

    def test_no_inputs_fails_validation(self):
        with self.assertRaises(ValidationError):
            self.check_clean()


class USAJobsApplicationLinkTestCase(ApplicationLinkTestCaseMixin, TestCase):
    link_cls = USAJobsApplicationLink

    def setUp(self):
        super(USAJobsApplicationLinkTestCase, self).setUp()
        self.applicant_type = mommy.make(ApplicantType)

    def test_all_fields_passes_validation(self):
        self.check_clean(
            announcement_number='abc123',
            url='http://www.xyz',
            applicant_type=self.applicant_type
        )

    def test_requires_url(self):
        with self.assertRaises(ValidationError):
            self.check_clean(
                announcement_number='abc123',
                url='this-is-not-a-url',
                applicant_type=self.applicant_type
            )


class EmailApplicationLinkTestCase(ApplicationLinkTestCaseMixin, TestCase):
    link_cls = EmailApplicationLink

    def test_all_fields_passes_validation(self):
        self.check_clean(
            address='user@example.com',
            label='Heading',
            description='Description'
        )

    def test_requires_address(self):
        with self.assertRaises(ValidationError):
            self.check_clean(
                address='this-is-not-an-email-address',
                label='Heading',
                description='Description'
            )

    def test_description_optional(self):
        self.check_clean(
            address='user@example.com',
            label='Heading'
        )

    def test_mailto_link(self):
        job = mommy.prepare(
            JobListingPage,
            title='This is a page title!',
            description='This is a page description'
        )

        address = 'user@example.com'
        link = EmailApplicationLink(address=address, job_listing=job)

        self.assertEqual(
            link.mailto_link,
            'mailto:{}?subject=Application for Position: {}'.format(
                address,
                'This%20is%20a%20page%20title%21'
            )
        )
