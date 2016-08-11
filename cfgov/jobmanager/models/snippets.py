from __future__ import absolute_import

from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class ApplicantTypeSnippet(models.Model):
    applicant_type_label = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['applicant_type_label']
        verbose_name = 'Job applicant type'
        verbose_name_plural = 'Job applicant types'

    panels = [
        FieldPanel('applicant_type_label'),
        FieldPanel('description'),
        FieldPanel('active'),
    ]

    def __unicode__(self):
        return self.applicant_type_label
