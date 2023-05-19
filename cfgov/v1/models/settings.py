from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)


@register_setting
class CFPBGuideSettings(BaseGenericSetting):
    url = models.URLField(
        help_text="Enter the URL for the internal CFPB Wagtail editor guide.",
        null=True,
        blank=True,
    )

    panels = [
        FieldPanel("url", heading="URL"),
    ]

    class Meta:
        verbose_name = "CFPB Guide"
