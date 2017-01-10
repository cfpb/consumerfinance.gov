from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from wagtail.wagtailcore.models import Site
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class WorkflowDestinationSetting(BaseSetting):
    destination = models.ForeignKey(Site, related_name='workflow_destination',
                                    null=True, default=None)
