# -*- coding: utf-8 -*-
# from __future__ import absolute_import, unicode_literals
from six.moves import html_parser as HTMLParser

from django.db import models
# from django import forms
# from django.apps import apps
# from django.contrib.auth.models import User
# from django.core.exceptions import ObjectDoesNotExist
# from django.utils.text import slugify
# from django.utils import html
# from django.utils.functional import cached_property

# from wagtail.wagtailadmin.edit_handlers import (
#     FieldPanel, FieldRowPanel, MultiFieldPanel
# )
# from wagtail.wagtailcore.blocks.stream_block import StreamValue
# from wagtail.wagtailcore.fields import RichTextField
# from wagtail.wagtailcore.models import Page
# from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

# from v1.util.migrations import get_or_create_page

html_parser = HTMLParser.HTMLParser()


class Section(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    contents = models.TextField(blank=True)


class Subpart(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    version = models.ForeignKey('EffectiveVersion')
    sections = models.ForeignKey(Section, blank=True, null=True)


class EffectiveVersion(models.Model):
    authority = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    effecitve_date = models.DateField(blank=True, null=True)
    part = models.ForeignKey('Part', blank=True, null=True)
    subparts = models.ForeignKey(Subpart, blank=True, null=True)


class Part(models.Model):
    cfr_title = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    letter_code = models.CharField(max_length=10)
    versions = models.ForeignKey(EffectiveVersion, blank=True, null=True)

    def get_parts_with_effective_version(self):
        pass

    def get_current_effective_version(self):
        pass
