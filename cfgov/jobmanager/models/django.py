from __future__ import absolute_import

import re

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags


class ApplicantType(models.Model):
    applicant_type = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.applicant_type

    class Meta:
        ordering = ['applicant_type']


class Grade(models.Model):
    grade = models.CharField(max_length=32)
    slug = models.SlugField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.grade

    class Meta:
        ordering = ['grade']


class JobCategory(models.Model):
    job_category = models.CharField(max_length=255)
    slug = models.SlugField()
    blurb = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.job_category

    class Meta:
        ordering = ['job_category']


class Location(models.Model):
    description = models.CharField(max_length=128)
    slug = models.SlugField()
    region = models.CharField(max_length=2)
    region_long = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.region

    class Meta:
        ordering = ['region']

    def job_count(self):
        return self.job_set.filter().count()


class FellowshipUpdateList(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    likes_design = models.BooleanField(default=False)
    likes_cybersecurity = models.BooleanField(default=False)
    likes_development = models.BooleanField(default=False)
    likes_data = models.BooleanField(default=False)

    def __unicode__(self):
        return self.first_name
