from __future__ import print_function

from datetime import timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.encoding import force_str
from wagtail.wagtailcore.models import Page

from jobmanager.models.django import Job
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import (
    EmailApplicationLink, GradePanel, RegionPanel, USAJobsApplicationLink
)


class JobConverter(object):
    def __init__(self, parent_slug, commit=False):
        self.parent = Page.objects.get(slug=parent_slug)
        print('using parent page {}'.format(self.parent))

        self.commit = commit
        self.user = User.objects.get(username='admin')

    def convert(self, job):
        page, creating = self.get_or_init_page(job.slug)

        self.set_page_attributes(page, job)

        if self.commit:
            if creating:
                self.parent.add_child(instance=page)
                print('created page {}, slug {}'.format(page.path, page.slug))
            else:
                print('updating page {}, slug {}'.format(page.path, page.slug))

        panels = []
        panels.extend(self.make_email_link_panels(page, job))
        panels.extend(self.make_usajobs_link_panels(page, job))
        panels.extend(self.make_grade_panels(page, job))
        panels.extend(self.make_region_panels(page, job))

        if self.commit:
            for panel in panels:
                panel.save()

            revision = page.save_revision(user=self.user)
            revision.publish()

        return page

    @staticmethod
    def get_or_init_page(slug):
        try:
            return (JobListingPage.objects.get(slug=slug), False)
        except JobListingPage.DoesNotExist:
            return (JobListingPage(slug=slug), True)

    @staticmethod
    def set_page_attributes(page, job):
        attributes = {
            'show_in_menus': False,
            'title': job.title,
            'depth': 3,
            'description': job.description or job.title,
            'open_date': job.open_date,
            'close_date': job.close_date,
            'salary_min': job.salary_min or 0,
            'salary_max': job.salary_max or 0,
            'division': job.category,
        }

        for k, v in attributes.items():
            setattr(page, k, v)

    def make_email_link_panels(self, page, job):
        return [
            EmailApplicationLink(
                job_listing=page,
                address=at.announcement_email,
                label=at.application_type.applicant_type,
                description=at.application_type.description
            ) for at in job.jobapplicanttype_set.filter(is_usajobs=False)
        ]

    def make_usajobs_link_panels(self, page, job):
        applicant_types = job.jobapplicanttype_set.filter(is_usajobs=True)
        if not all(at.announcement_number for at in applicant_types):
            print('warning, adding empty usajobs announcement number')

        return [
            USAJobsApplicationLink(
                job_listing=page,
                announcement_number=at.announcement_number,
                url=at.usajobs_url,
                applicant_type=at.application_type,
            ) for at in applicant_types
        ]

    def make_grade_panels(self, page, job):
        return [
            GradePanel(job_listing=page, grade=grade)
            for grade in job.grades.all()
        ]

    def make_region_panels(self, page, job):
        return [
            RegionPanel(job_listing=page, region=region)
            for region in job.locations.all()
        ]


class Command(BaseCommand):
    help = 'Converts Jobmanager Django Job models to Wagtail pages'

    def add_arguments(self, parser):
        parser.add_argument('parent', help='Slug of parent page')
        parser.add_argument('-d', '--dry-run', action='store_true',
                            help='Create pages but do not persist them')
        parser.add_argument('--limit', type=int, help='Limit', default=None)
        parser.add_argument('--pk', help='Specific page to convert',
                            type=int, default=None)

    def handle(self, *args, **options):
        parent = options['parent']
        commit = not options['dry_run']
        limit = options['limit']
        pk = options['pk']

        date_cutoff = timezone.now().date() - timedelta(days=30)
        jobs = Job.objects.filter(close_date__gte=date_cutoff)

        if pk:
            jobs = jobs.filter(pk=pk)
        elif limit:
            jobs = jobs[:limit]

        converter = JobConverter(parent_slug=parent, commit=commit)

        with transaction.atomic():
            for i, job in enumerate(jobs):
                print('{}/{} converting job {} ({})'.format(
                    i + 1,
                    jobs.count(),
                    force_str(job.title),
                    force_str(job.slug)
                ))

                converter.convert(job)
