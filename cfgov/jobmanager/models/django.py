from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.six import python_2_unicode_compatible

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


@python_2_unicode_compatible
class ApplicantType(models.Model):
    applicant_type = models.CharField(max_length=255)
    display_title = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    description = models.TextField()

    def __str__(self):
        return self.applicant_type

    class Meta:
        ordering = ['applicant_type']


@python_2_unicode_compatible
class Grade(models.Model):
    grade = models.CharField(max_length=32)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()

    def __str__(self):
        return self.grade

    class Meta:
        ordering = ['grade']

    def __lt__(self, other):
        return self.grade < other.grade

    def __gt__(self, other):
        return self.grade > other.grade


@python_2_unicode_compatible
class JobCategory(models.Model):
    job_category = models.CharField(max_length=255)
    blurb = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.job_category

    class Meta:
        ordering = ['job_category']


@python_2_unicode_compatible
class ServiceType(models.Model):
    service_type = models.CharField(max_length=255)

    def __str__(self):
        return self.service_type

    class Meta:
        ordering = ['service_type']


@python_2_unicode_compatible
class JobLength(models.Model):
    job_length = models.CharField(max_length=255)

    def __str__(self):
        return self.job_length

    class Meta:
        ordering = ['job_length']


@python_2_unicode_compatible
class JobLocation(ClusterableModel):
    abbreviation = models.CharField(
        max_length=2,
        primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('abbreviation',)


class Region(JobLocation):
    panels = [
        FieldPanel('abbreviation'),
        FieldPanel('name'),
        InlinePanel('states', label="States"),
        InlinePanel('cities', label="Cities"),
    ]


class Office(JobLocation):
    panels = [
        FieldPanel('abbreviation'),
        FieldPanel('name'),
        InlinePanel('cities', label="Office location", max_num=1),
    ]


@python_2_unicode_compatible
class State(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="State name")
    abbreviation = models.CharField(
        max_length=2,
        primary_key=True)
    region = ParentalKey(
        'Region',
        related_name="states")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('abbreviation',)


@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="City name")
    state = models.ForeignKey(
        State,
        null=False,
        blank=False,
        default=None,
        related_name='cities')
    location = ParentalKey(
        'JobLocation',
        related_name='cities'
    )

    class Meta:
        ordering = ('state_id', 'name')

    def __str__(self):
        return '{}, {}'.format(self.name, self.state.abbreviation)
