from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class ApplicantType(models.Model):
    applicant_type = models.CharField(max_length=255)
    display_title = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    description = models.TextField()

    def __unicode__(self):
        return self.applicant_type

    class Meta:
        ordering = ['applicant_type']


class Grade(models.Model):
    grade = models.CharField(max_length=32)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()

    def __unicode__(self):
        return self.grade

    class Meta:
        ordering = ['grade']


class JobCategory(models.Model):
    job_category = models.CharField(max_length=255)
    blurb = RichTextField(null=True, blank=True)

    def __unicode__(self):
        return self.job_category

    class Meta:
        ordering = ['job_category']


class ServiceType(models.Model):
    service_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.service_type

    class Meta:
        ordering = ['service_type']


class JobLength(models.Model):
    job_length = models.CharField(max_length=255)

    def __unicode__(self):
        return self.job_length

    class Meta:
        ordering = ['job_length']


class JobLocation(ClusterableModel):
    abbreviation = models.CharField(
        max_length=2,
        primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
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

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('abbreviation',)


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

    def __unicode__(self):
        return '{}, {}'.format(self.name, self.state.abbreviation)
