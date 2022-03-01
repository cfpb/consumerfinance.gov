from django.db import models
from django.utils.http import urlquote

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable

from modelcluster.fields import ParentalKey

from jobmanager.models.django import ApplicantType, Grade
from jobmanager.models.pages import JobListingPage


class EmailApplicationLink(Orderable, models.Model):
    address = models.EmailField()
    label = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    job_listing = ParentalKey(JobListingPage, related_name="email_application_links")

    panels = [
        FieldPanel("address"),
        FieldPanel("label"),
        FieldPanel("description"),
    ]

    @property
    def mailto_link(self):
        return "mailto:{0}?subject=Application for Position: {1}".format(
            self.address, urlquote(self.job_listing.title)
        )


class USAJobsApplicationLink(Orderable, models.Model):
    announcement_number = models.CharField(max_length=128)
    url = models.URLField(max_length=255)
    applicant_type = models.ForeignKey(
        ApplicantType,
        on_delete=models.CASCADE,
        related_name="usajobs_application_links",
    )

    job_listing = ParentalKey(JobListingPage, related_name="usajobs_application_links")

    panels = [
        FieldPanel("announcement_number"),
        FieldPanel("url"),
        FieldPanel("applicant_type"),
    ]


class GradePanel(Orderable, models.Model):
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, related_name="grade_panels"
    )
    job_listing = ParentalKey(JobListingPage, related_name="grades")

    def __str__(self):
        return str(self.grade)

    class Meta:
        ordering = ("grade",)

    panels = [
        FieldPanel("grade"),
    ]
