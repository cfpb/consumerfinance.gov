# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from regulations3k.models.fields import RegDownTextField


class Section(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    contents = RegDownTextField(blank=True)

    def __str__(self):
        return "{} {}".format(self.label, self.title)


class Subpart(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    version = models.ForeignKey(
        'EffectiveVersion', blank=True, null=True,
        related_name='subpart_version')
    sections = models.ForeignKey(Section, blank=True, null=True)

    def __str__(self):
        return "{} {} ({})".format(self.label, self.title, self.version)


class EffectiveVersion(models.Model):
    authority = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    effecitve_date = models.DateField(blank=True, null=True)
    part = models.ForeignKey('Part', blank=True, null=True)
    subparts = models.ForeignKey(Subpart, blank=True, null=True)

    def __str__(self):
        return "{} {} ({})".format(
            self.part, self.subparts, self.effecitve_date)


class Part(models.Model):
    cfr_title = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    letter_code = models.CharField(max_length=10)
    versions = models.ForeignKey(
        EffectiveVersion, blank=True, null=True,
        related_name='part_version')

    def __str__(self):
        return self.crf_title

    def get_parts_with_effective_version(self):
        pass

    def get_current_effective_version(self):
        pass
