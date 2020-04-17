from wagtail.core import blocks

from jobmanager.models import JobListingPage
from v1.util.util import extended_strftime


class JobListingsMixin:
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update({
            'jobs': self.get_job_listings(),
            'no_jobs_message': (
                'There are no current openings at this time.'
            ),
        })
        return context

    def get_job_listings(self):
        return JobListingPage.objects.open()


class JobListingList(JobListingsMixin, blocks.StructBlock):
    more_jobs_page = blocks.PageChooserBlock(
        help_text='Link to full list of jobs'
    )

    def get_job_listings(self):
        return super().get_job_listings()[:5]

    class Meta:
        icon = 'list-ul'
        template = 'jobmanager/job_listing_list.html'


class JobListingTable(JobListingsMixin, blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        jobs = context['jobs']
        request = context.get('request')

        header = [['TITLE', 'GRADE', 'POSTING CLOSES', 'LOCATION']]
        data = [
            [
                '<a href="%s">%s</a>' % (
                    job.get_url(request=request),
                    job.title,
                ),
                ', '.join(map(str, job.grades.all())),
                extended_strftime(job.close_date, '%_m %_d, %Y'),
                str(job.location),
            ] for job in jobs
        ]

        return {
            'value': {
                'data': header + data,
                'empty_table_msg': context['no_jobs_message'],
                'first_row_is_table_header': True,
                'has_data': bool(data),
                'is_stacked': True,
            },
        }

    def get_job_listings(self):
        return super().get_job_listings() \
            .select_related('location') \
            .prefetch_related('grades__grade')

    class Meta:
        icon = 'table'
        template = '_includes/organisms/table.html'
