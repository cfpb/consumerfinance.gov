from __future__ import absolute_import

from django.core.exceptions import ValidationError
from django.db import models
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, ObjectList
)

from jobmanager.models.django import Grade, JobCategory, Location
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
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True)
    region = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)

    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('division', classname='full'),
            FieldPanel('grade', classname='full'),
            FieldPanel('region', classname='full'),
            FieldRowPanel([
                FieldPanel('open_date', classname='col6'),
                FieldPanel('close_date', classname='col6'),
            ]),
            FieldRowPanel([
                FieldPanel('salary_min', classname='col6'),
                FieldPanel('salary_max', classname='col6'),
            ]),
        ], heading='Details'),
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

    edit_handler = ObjectList(content_panels, heading='Content')

    template = 'job-description-page/index.html'
