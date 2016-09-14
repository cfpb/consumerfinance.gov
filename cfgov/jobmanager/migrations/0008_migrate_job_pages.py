# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from django.apps import apps as imported_apps
from django.db import migrations, transaction
from django.utils import timezone

from v1.util.migrations import get_or_create_page, get_page


class JobConverter(object):
    def __init__(self, parent, apps=None):
        self.parent = parent
        self.apps = apps or imported_apps

    def convert(self, job):
        page_attributes = self.get_page_attributes(job)

        page = get_or_create_page(
            apps=self.apps,
            page_cls_app='jobmanager',
            page_cls_name='JobListingPage',
            title=job.title,
            slug=job.slug,
            parent_page=self.parent,
            **page_attributes
        )

        panels = []
        panels.extend(self.make_email_link_panels(page, job))
        panels.extend(self.make_usajobs_link_panels(page, job))
        panels.extend(self.make_grade_panels(page, job))
        panels.extend(self.make_region_panels(page, job))

        for panel in panels:
            panel.save()

        return page

    def get_or_init_page(self, slug):
        page_cls = self.apps.get_model('jobmanager', 'JobListingPage')

        try:
            return (page_cls.objects.get(slug=slug), False)
        except page_cls.DoesNotExist:
            return (page_cls(slug=slug), True)

    @staticmethod
    def get_page_attributes(job):
        return {
            'description': job.description or job.title,
            'open_date': job.open_date,
            'close_date': job.close_date,
            'salary_min': job.salary_min or 0,
            'salary_max': job.salary_max or 0,
            'division': job.category,
        }

    def make_email_link_panels(self, page, job):
        link_cls = self.apps.get_model('jobmanager', 'EmailApplicationLink')

        return [
            link_cls(
                job_listing=page,
                address=at.announcement_email,
                label=at.application_type.applicant_type,
                description=at.application_type.description
            ) for at in job.jobapplicanttype_set.filter(is_usajobs=False)
        ]

    def make_usajobs_link_panels(self, page, job):
        applicant_types = job.jobapplicanttype_set.filter(is_usajobs=True)
        if not all(at.announcement_number for at in applicant_types):
            raise ValueError('empty usajobs announcement number')

        link_cls = self.apps.get_model('jobmanager', 'USAJobsApplicationLink')

        return [
            link_cls(
                job_listing=page,
                announcement_number=at.announcement_number,
                url=at.usajobs_url,
                applicant_type=at.application_type,
            ) for at in applicant_types
        ]

    def make_grade_panels(self, page, job):
        panel_cls = self.apps.get_model('jobmanager', 'GradePanel')

        return [
            panel_cls(job_listing=page, grade=grade)
            for grade in job.grades.all()
        ]

    def make_region_panels(self, page, job):
        panel_cls = self.apps.get_model('jobmanager', 'RegionPanel')

        return [
            panel_cls(job_listing=page, region=region)
            for region in job.locations.all()
        ]


@transaction.atomic
def migrate_job_pages(apps, schema_editor):
    Job = apps.get_model('jobmanager', 'Job')
    date_cutoff = timezone.now().date() - timedelta(days=180)
    jobs = Job.objects.filter(close_date__gte=date_cutoff)

    careers_page = get_page(apps, slug='careers')
    converter = JobConverter(parent=careers_page, apps=apps)

    for job in jobs:
        converter.convert(job)


class Migration(migrations.Migration):
    dependencies = [
        ('jobmanager', '0007_create_careers_pages'),
    ]

    operations = [
        migrations.RunPython(migrate_job_pages, migrations.RunPython.noop),
    ]
