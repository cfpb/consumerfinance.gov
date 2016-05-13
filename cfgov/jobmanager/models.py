from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import strip_tags
from datetime import datetime

import re

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

class Job(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('JobCategory')
    salary_min = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    salary_max = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    hourly = models.BooleanField(default=False)
    grades = models.ManyToManyField(Grade, verbose_name="list of grades")
    applicant_types = models.ManyToManyField('ApplicantType', through='JobApplicantType')
    locations = models.ManyToManyField(Location, verbose_name="list of locations")
    open_date = models.DateField()
    close_date = models.DateField()
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()

    open_graph_title = models.CharField(max_length=255, blank=True,
        help_text='If blank, uses the title field above')
    open_graph_description = models.CharField(max_length=1000, blank=True,
        help_text='If blank, uses the description field above')
    open_graph_image_url = models.URLField(blank=True,
        help_text='A full URL to an image. If blank, uses the CFPB logo.')

    twitter_text = models.CharField(max_length=100, blank=True,
        help_text='Custom text for Twitter shares. If blank, uses the first \
        100 characters of the title field above')

    utm_campaign = models.CharField(max_length=100, blank=True,
        verbose_name = 'UTM campaign',
        help_text = 'Use to add a UTM campaign code to the share links \
        on this page.')

    def __unicode__(self):
        return '%s (%s): %s' % (self.title, self.open_date, self.category)

    class Meta:
        ordering = ['close_date', 'title']

    def get_absolute_url(self):
        return reverse('careers:detail', kwargs={'slug': self.slug})

    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
        self.date_modified = datetime.now()
        super(Job, self).save()

    def clean(self):
        normalized_slug = re.sub(r'-\d*$', '', self.slug)
        similar = Job.objects.filter(slug__startswith=normalized_slug)
        if similar:
            # might cause errors if we still have slug duplicates in db
            d = {}
            for i in similar:
                d[i.slug] = i
            if self.slug in d and not (self.id and d[self.slug].id == self.id):
                new_slug = normalized_slug
                i = 0
                while new_slug in d and d[new_slug].id != self.id:
                    i += 1
                    new_slug = normalized_slug + '-' + str(i)
                self.slug = new_slug

    def get_open_graph_title(self):
        if self.open_graph_title:
            title = self.open_graph_title
        else:
            title = self.title

        return strip_tags(title)

    def get_open_graph_description(self):
        if self.open_graph_description:
            description = self.open_graph_description
        else:
            description = self.description[:500]

        return strip_tags(description)

    def get_twitter_text(self):
        if self.twitter_text:
            text = self.twitter_text
        else:
            if len(self.title) <= 103:
                text = self.title
            else:
                text = '%s...' % self.title[:100]

        return strip_tags(text)

    @property
    def location_names(self):
        return [l.region_long for l in self.locations.all()]


class JobApplicantType(models.Model):
    application_type = models.ForeignKey(ApplicantType)
    job = models.ForeignKey(Job)
    is_usajobs = models.BooleanField(default=True)
    usajobs_url = models.URLField(max_length=255, null=True, blank=True)
    announcement_number = models.CharField(max_length=128, null=True, blank=True)
    announcement_email = models.CharField(max_length=128, null=True, blank=True)
    announcement_close_time = models.TimeField(null=True, blank=True)

    def __unicode__(self):
        return u'%s (%s) %s' % (self.job, self.announcement_number, self.application_type)

    class Meta:
        ordering = ['job']






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






