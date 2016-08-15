from __future__ import absolute_import

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Orderable

from jobmanager.models.django import ApplicantType
from jobmanager.models.pages import JobListingPage


class EmailApplicationLink(Orderable, models.Model):
    address = models.EmailField()
    label = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    job_listing = ParentalKey(
        JobListingPage,
        related_name='email_application_links'
    )

    panels = [
        FieldPanel('address'),
        FieldPanel('label'),
        FieldPanel('description'),
    ]


class USAJobsApplicationLink(Orderable, models.Model):
    announcement_number = models.CharField(max_length=128)
    url = models.URLField(max_length=255)
    applicant_type = models.ForeignKey(
        ApplicantType,
        related_name='usajobs_application_links',
    )

    job_listing = ParentalKey(
        JobListingPage,
        related_name='usajobs_application_links'
    )

    panels = [
        FieldPanel('announcement_number'),
        FieldPanel('url'),
        FieldPanel('applicant_type'),
    ]
