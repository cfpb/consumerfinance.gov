import unittest
from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from wagtail.core.models import Locale, Page

from model_bakery import baker

from jobmanager.models.django import ApplicantType, Grade
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import (
    EmailApplicationLink,
    GradePanel,
    USAJobsApplicationLink,
)


class GradePanelTests(unittest.TestCase):
    def test_str(self):
        grade = Grade(grade="53", salary_min=1, salary_max=100)
        self.assertEqual(
            str(GradePanel(grade=grade, job_listing_id=123)), "53"
        )


class ApplicationLinkTestCaseMixin:
    link_cls = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.root = Page.objects.get(slug="root")

    def setUp(self):
        locale = Locale.objects.get(pk=1)
        self.job_listing = baker.prepare(
            JobListingPage, description="foo", locale=locale
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
        super().setUp()
        self.applicant_type = baker.make(ApplicantType)

    def test_all_fields_passes_validation(self):
        self.check_clean(
            announcement_number="abc123",
            url="http://www.xyz",
            applicant_type=self.applicant_type,
        )

    def test_requires_url(self):
        with self.assertRaises(ValidationError):
            self.check_clean(
                announcement_number="abc123",
                url="this-is-not-a-url",
                applicant_type=self.applicant_type,
            )


class EmailApplicationLinkTestCase(ApplicationLinkTestCaseMixin, TestCase):
    link_cls = EmailApplicationLink

    def test_all_fields_passes_validation(self):
        self.check_clean(
            address="user@example.com",
            label="Heading",
            description="Description",
        )

    def test_requires_address(self):
        with self.assertRaises(ValidationError):
            self.check_clean(
                address="this-is-not-an-email-address",
                label="Heading",
                description="Description",
            )

    def test_description_optional(self):
        self.check_clean(address="user@example.com", label="Heading")

    def test_mailto_link(self):
        job = baker.prepare(
            JobListingPage,
            title="This is a page title!",
            description="This is a page description",
        )

        address = "user@example.com"
        link = EmailApplicationLink(address=address, job_listing=job)

        self.assertEqual(
            link.mailto_link,
            "mailto:{}?subject=Application for Position: {}".format(
                address, "This%20is%20a%20page%20title%21"
            ),
        )
