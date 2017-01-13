from django.db import models

from wagtail.wagtailcore.models import Site
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class WorkflowDestinationSetting(BaseSetting):
    destination = models.ForeignKey(Site, related_name='workflow_destination',
                                    null=True, default=None)
