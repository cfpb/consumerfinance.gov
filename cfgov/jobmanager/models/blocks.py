from django.template.loader import render_to_string
from django.utils import timezone
from v1.atomic_elements.organisms import ModelList, ModelTable


class OpenJobListingsMixin(object):
    def filter_queryset(self, qs, value):
        qs = super(OpenJobListingsMixin, self).filter_queryset(qs, value)
        today = timezone.now().date()
        return qs.filter(open_date__lte=today, close_date__gte=today)


class JobListingList(OpenJobListingsMixin, ModelList):
    model = 'jobmanager.JobListingPage'
    ordering = ('close_date', 'title')

    def render(self, value):
        template = '_includes/organisms/job-listing-list.html'
        return render_to_string(template, {
            'careers': self.get_queryset(value),
        })


class JobListingTable(OpenJobListingsMixin, ModelTable):
    model = 'jobmanager.JobListingPage'
    ordering = ('close_date', 'title')

    fields = ['title', 'grades', 'close_date', 'regions']
    field_headers = ['TITLE', 'GRADE', 'POSTING CLOSES', 'REGION']

    def make_grades_value(self, value):
        return ', '.join(sorted(g.grade.grade for g in value.all()))

    def make_close_date_value(self, value):
        return value.strftime('%b %d, %Y').upper()

    def make_regions_value(self, value):
        return ', '.join(sorted(r.region.region_long for r in value.all()))
