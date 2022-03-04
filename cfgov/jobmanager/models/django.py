from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class ApplicantType(models.Model):
    applicant_type = models.CharField(max_length=255)
    display_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.display_title or self.applicant_type

    class Meta:
        ordering = ["applicant_type"]

    def __lt__(self, other):
        return self.applicant_type < other.applicant_type

    def __gt__(self, other):
        return self.applicant_type > other.applicant_type


class Grade(models.Model):
    grade = models.CharField(max_length=32)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()

    def __str__(self):
        return self.grade

    class Meta:
        ordering = ["grade"]

    def __lt__(self, other):
        return self.grade < other.grade

    def __gt__(self, other):
        return self.grade > other.grade


class JobCategory(models.Model):
    job_category = models.CharField(max_length=255)
    blurb = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.job_category

    class Meta:
        ordering = ["job_category"]


class ServiceType(models.Model):
    service_type = models.CharField(max_length=255)

    def __str__(self):
        return self.service_type

    class Meta:
        ordering = ["service_type"]


class JobLength(models.Model):
    job_length = models.CharField(max_length=255)

    def __str__(self):
        return self.job_length

    class Meta:
        ordering = ["job_length"]


class Region(ClusterableModel):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=2, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("abbreviation",)

    panels = [
        FieldPanel("name"),
        FieldPanel("abbreviation"),
        InlinePanel("states", label="States"),
        InlinePanel("major_cities", label="Major cities"),
    ]


class State(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=2, primary_key=True)
    region = ParentalKey(
        Region, related_name="states", on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("abbreviation",)

    def __lt__(self, other):
        return self.abbreviation < other.abbreviation

    def __gt__(self, other):
        return self.abbreviation > other.abbreviation


class AbstractCity(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    class Meta:
        abstract = True
        ordering = ("state", "name")

    def __str__(self):
        return ", ".join((self.name, self.state_id))


class Office(AbstractCity):
    abbreviation = models.CharField(max_length=2, primary_key=True)

    class Meta:
        ordering = ("abbreviation",)


class MajorCity(AbstractCity):
    region = ParentalKey(
        Region, on_delete=models.PROTECT, related_name="major_cities"
    )
