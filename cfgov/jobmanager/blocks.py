from wagtail.core import blocks

from jobmanager.models import JobListingPage


class JobListingList(blocks.StructBlock):
    more_jobs_page = blocks.PageChooserBlock(
        help_text='Link to full list of jobs'
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        jobs = JobListingPage.objects.open()[:5]
        request = context.get('request')

        context['value'] = {
            'jobs': [
                {
                    'title': job.title,
                    'url': job.get_url(request=request),
                    'close_date': job.close_date,
                } for job in jobs
            ],
            'more_jobs_url': value['more_jobs_page'].get_url(request=request),
        }

        return context

    class Meta:
        icon = 'list-ul'
        template = 'jobmanager/job_listing_list.html'


class JobListingTable(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        jobs = JobListingPage.objects.open().prefetch_related('grades__grade')

        request = context.get('request')

        context['value'] = {
            'jobs': [
                {
                    'title': job.title,
                    'url': job.get_url(request=request),
                    'grades': list(map(str, job.grades.all())),
                    'close_date': job.close_date,
                    'offices': [
                        {
                            'name': office.name,
                            'state_id': office.state_id,
                        } for office in job.offices.all()
                    ],
                    'regions': [
                        {
                            'name': region.name,
                        } for region in job.regions.all()
                    ],
                } for job in jobs
            ],
        }

        return context

    class Meta:
        icon = 'table'
        template = 'jobmanager/job_listing_table.html'
