from __future__ import absolute_import

from django.template.loader import render_to_string
from django.utils import timezone
from v1.atomic_elements import organisms
from wagtail.wagtailcore import blocks


class OpenJobListingsMixin(object):
    def filter_queryset(self, qs, value):
        qs = super(OpenJobListingsMixin, self).filter_queryset(qs, value)

        # Hide any jobs that have not been published.
        qs = qs.filter(live=True)

        if value.get('hide_closed'):
            today = timezone.now().date()
            qs = qs.filter(open_date__lte=today, close_date__gte=today)

        return qs


class JobListingList(OpenJobListingsMixin, organisms.ModelList):
    model = 'jobmanager.JobListingPage'
    ordering = ('close_date', 'title')

    heading = blocks.CharBlock(required=False, help_text='List heading')
    more_jobs_page = blocks.PageChooserBlock(
        help_text='Link to full list of jobs'
    )
    more_jobs_text = blocks.CharBlock(
        required=False,
        help_text='Text to show on link to full list of jobs'
    )

    hide_closed = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text=(
            'Whether to hide jobs that are not currently open '
            '(jobs will automatically update)'
        )
    )

    def render(self, value):
        value['careers'] = self.get_queryset(value)
        template = '_includes/organisms/job-listing-list.html'
        return render_to_string(template, value)


class JobListingTable(OpenJobListingsMixin, organisms.ModelTable):
    model = 'jobmanager.JobListingPage'
    ordering = ('close_date', 'title')

    hide_closed = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text=(
            'Whether to hide jobs that are not currently open '
            '(jobs will automatically update)'
        )
    )

    fields = ['title', 'grades', 'close_date', 'regions']
    field_headers = ['TITLE', 'GRADE', 'POSTING CLOSES', 'REGION']

    def make_title_value(self, instance, value):
        return '<a href="{}">{}</a>'.format(instance.url, value)

    def make_grades_value(self, instance, value):
        return ', '.join(sorted(g.grade.grade for g in value.all()))

    def make_close_date_value(self, instance, value):
        return value.strftime('%b %d, %Y').upper()

    def make_regions_value(self, instance, value):
        return ', '.join(sorted(r.region.region_long for r in value.all()))
