from __future__ import absolute_import

from django.db import models


class ApplicantType(models.Model):
    applicant_type = models.CharField(max_length=255)
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
    blurb = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.job_category

    class Meta:
        ordering = ['job_category']


class Location(models.Model):
    description = models.CharField(max_length=128)
    region = models.CharField(max_length=2)
    region_long = models.CharField(max_length=255)

    def __unicode__(self):
        return self.region

    class Meta:
        ordering = ['region']


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
