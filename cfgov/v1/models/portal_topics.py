# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class PortalTopicTag(TaggedItemBase):
    content_object = ParentalKey(
        'v1.PortalTopic',
        related_name='tagged_portal_topic',
        null=True,
        on_delete=models.SET_NULL)


@python_2_unicode_compatible
@register_snippet
class PortalTopic(ClusterableModel):
    heading = models.CharField(max_length=255, blank=True)
    heading_es = models.CharField(max_length=255, blank=True)

    tags = TaggableManager(
        through=PortalTopicTag,
        blank=True,
        help_text='Tags are used to identify and organize portal topic pages.'
    )

    def __str__(self):
        return self.heading


class PortalCategoryTag(TaggedItemBase):
    content_object = ParentalKey(
        'v1.PortalCategory',
        related_name='tagged_portal_category',
        null=True,
        on_delete=models.SET_NULL)


@python_2_unicode_compatible
@register_snippet
class PortalCategory(ClusterableModel):
    heading = models.CharField(max_length=255, blank=True)
    heading_es = models.CharField(max_length=255, blank=True)

    tags = TaggableManager(
        through=PortalCategoryTag,
        blank=True,
        help_text=(
            'Tags are used to identify and organize portal see-all pages.')
    )

    class Meta:
        verbose_name_plural = "portal categories"

    def __str__(self):
        return self.heading
