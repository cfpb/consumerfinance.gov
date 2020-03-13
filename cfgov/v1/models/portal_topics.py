# -*- coding: utf-8 -*-

from django.db import models

from wagtail.snippets.models import register_snippet

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


@register_snippet
class PortalTopic(ClusterableModel):
    heading = models.CharField(max_length=255, blank=True)
    heading_es = models.CharField(max_length=255, blank=True)

    tags = TaggableManager(
        through=PortalTopicTag,
        blank=True,
        help_text='Tags are used to identify and organize portal topic pages.'
    )

    def featured_answers(self, language):
        return self.answerpage_set.filter(
            language=language,
            featured=True).order_by('featured_rank')

    def title(self, language='en'):
        if language == 'es':
            return self.heading_es
        return self.heading

    def __str__(self):
        return self.heading


class PortalCategoryTag(TaggedItemBase):
    content_object = ParentalKey(
        'v1.PortalCategory',
        related_name='tagged_portal_category',
        null=True,
        on_delete=models.SET_NULL)


@register_snippet
class PortalCategory(ClusterableModel):
    heading = models.CharField(max_length=255, blank=True)
    heading_es = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(
        default=0,
        help_text="Controls sequence of categories in sidebar navigation.")
    tags = TaggableManager(
        through=PortalCategoryTag,
        blank=True,
        help_text=(
            'Tags are used to identify and organize portal see-all pages.')
    )

    class Meta:
        verbose_name_plural = "portal categories"
        ordering = ['display_order']

    def title(self, language='en'):
        if language == 'es':
            return self.heading_es

        return self.heading

    def __str__(self):
        return self.heading
