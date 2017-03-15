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


class JobRegion(models.Model):
    abbreviation = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('abbreviation',)
