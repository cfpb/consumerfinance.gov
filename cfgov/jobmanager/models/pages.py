from __future__ import absolute_import

from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, ObjectList,
    TabbedInterface
)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import PageManager

from jobmanager.models.django import JobCategory, JobLocation
from v1.models import CFGOVPage


class JobListingPage(CFGOVPage):
    description = RichTextField('Description')
    open_date = models.DateField('Open date')
    close_date = models.DateField('Close date')
    salary_min = models.DecimalField('Minimum salary', max_digits=11,
                                     decimal_places=2)
    salary_max = models.DecimalField('Maximum salary', max_digits=11,
                                     decimal_places=2)
    division = models.ForeignKey(JobCategory, on_delete=models.PROTECT,
                                 null=True)
    location = models.ForeignKey(JobLocation, related_name='job_listings',
                                 on_delete=models.PROTECT)
    allow_remote = models.BooleanField(
        default=False,
        help_text='Adds remote option to jobs with office locations.',
        verbose_name="Location can also be remote"
    )
    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('division', classname='full'),
            InlinePanel('grades', label='Grades'),
            FieldRowPanel([
                FieldPanel('open_date', classname='col6'),
                FieldPanel('close_date', classname='col6'),
            ]),
            FieldRowPanel([
                FieldPanel('salary_min', classname='col6'),
                FieldPanel('salary_max', classname='col6'),
            ]),
        ], heading='Details'),
        MultiFieldPanel([
            FieldPanel('location', classname='full'),
            FieldPanel('allow_remote', classname='full'),
        ], heading='Location'),
        FieldPanel('description', classname='full'),
        InlinePanel(
            'usajobs_application_links',
            label='USAJobs application links'
        ),
        InlinePanel(
            'email_application_links',
            label='Email application links'
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'job-description-page/index.html'

    objects = PageManager()

    def get_context(self, request, *args, **kwargs):
        context = super(JobListingPage, self).get_context(request)
        if hasattr(self.location, 'region'):
            context['states'] = [state.abbreviation for state in
                                 self.location.region.states.all()]
            context['location_type'] = 'region'
        else:
            context['states'] = []
            context['location_type'] = 'office'
        context['cities'] = self.location.cities.all()
        return context

    @property
    def ordered_grades(self):
        """Return a list of job grades in numerical order.

        Non-numeric grades are sorted alphabetically after numeric grades.
        """
        grades = set(g.grade.grade for g in self.grades.all())
        return sorted(grades, key=lambda g: int(g) if g.isdigit() else g)
