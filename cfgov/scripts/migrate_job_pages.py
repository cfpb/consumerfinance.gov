from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from wagtail.wagtailcore.models import Page

from jobmanager.models import (
    EmailApplicationLink, GradePanel, Job, JobListingPage, RegionPanel,
    USAJobsApplicationLink
)
from v1.tests.wagtail_pages.helpers import save_new_page


class JobConverter(object):
    def __init__(self, parent):
        self.parent = parent

    def convert(self, job):
        page_attributes = self.get_page_attributes(job)

        try:
            page = JobListingPage.objects.get(slug=job.slug)
        except JobListingPage.DoesNotExist:
            page = JobListingPage(
                title=job.title,
                slug=job.slug,
                **page_attributes
            )

            save_new_page(page, root=self.parent)

        panels = []
        panels.extend(self.make_email_link_panels(page, job))
        panels.extend(self.make_usajobs_link_panels(page, job))
        panels.extend(self.make_grade_panels(page, job))
        panels.extend(self.make_region_panels(page, job))

        for panel in panels:
            panel.save()

        return page

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
            raise ValueError('empty usajobs announcement number')

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


@transaction.atomic
def run():
    date_cutoff = timezone.now().date() - timedelta(days=180)
    jobs = Job.objects.filter(close_date__gte=date_cutoff)

    careers_page = Page.objects.get(slug='careers')
    converter = JobConverter(parent=careers_page)

    for job in jobs:
        converter.convert(job)


if '__main__' == __name__:
    run()
