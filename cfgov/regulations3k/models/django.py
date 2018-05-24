# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property

from wagtail.wagtailadmin.edit_handlers import FieldPanel


def sortable_label(label, separator='-'):
    """ Create a sortable tuple out of a label.
    Converts a dashed label into a tuple based on the following rules:
        - If a segment is numeric, it will get three leading zero places
        - If a segment is alphabetic and is already uppercase, it is
            returned as is.
        - If a segment is alphabetic but is not all uppercase, it is
            lowercased entirely.
        - Anything else is returned as-is.
    Intended to be used like `sorted(sections, key=Section.sortable_label)`
    """
    segments = []
    for segment in label.split(separator):
        if segment.isdigit():
            segments.append(segment.zfill(4))
        elif segment.isalpha() and segment.isupper():
            segments.append(segment)
        elif segment.isalpha():
            segments.append(segment.lower())
        else:
            segments.append(segment)
    return tuple(segments)


@python_2_unicode_compatible
class Part(models.Model):
    cfr_title_number = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    letter_code = models.CharField(max_length=10)

    panels = [
        FieldPanel('cfr_title_number'),
        FieldPanel('title'),
        FieldPanel('part_number'),
        FieldPanel('letter_code'),
        FieldPanel('chapter'),
    ]

    @property
    def cfr_title(self):
        return "{} CFR Part {} (Regulation {})".format(
            self.cfr_title_number, self.part_number, self.letter_code)

    def __str__(self):
        name = "12 CFR Part {}".format(self.part_number)
        if self.letter_code:
            name += " (Regulation {})".format(self.letter_code)
        return name

    class Meta:
        ordering = ['part_number']

    @cached_property
    def effective_version(self):
        """ Return the current effective version of the regulation.
        This selects based on effective_date being less than or equal to
        the current date and version is not a draft. """
        effective_version = self.versions.filter(
            draft=False,
            effective_date__lte=datetime.now()
        ).order_by(
            '-effective_date'
        ).first()
        return effective_version


@python_2_unicode_compatible
class EffectiveVersion(models.Model):
    authority = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    effective_date = models.DateField(blank=True, null=True)
    acquired = models.DateField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    part = models.ForeignKey(Part, related_name="versions")

    panels = [
        FieldPanel('authority'),
        FieldPanel('source'),
        FieldPanel('effective_date'),
        FieldPanel('part'),
        FieldPanel('draft'),
        FieldPanel('acquired'),
    ]

    def __str__(self):
        return "{}, effective {}".format(
            self.part, self.effective_date)

    class Meta:
        ordering = ['effective_date']
        default_related_name = 'version'


@python_2_unicode_compatible
class Subpart(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    version = models.ForeignKey(EffectiveVersion, related_name="subparts")

    panels = [
        FieldPanel('label'),
        FieldPanel('title'),
        FieldPanel('version'),
    ]

    def __str__(self):
        return "{} {}, effective {}".format(
            self.label, self.title, self.version.effective_date)

    @property
    def subpart_heading(self):
        """Keeping for now as possible hook into secondary nav"""
        return ''

    @property
    def section_range(self):
        if not self.sections.exists():
            return ''
        if 'Interp' in self.label:
            return ''
        if 'Append' in self.title:
            return ''
        if self.sections.first().section_number.isdigit():
            sections = sorted(
                self.sections.all(), key=lambda x: int(x.section_number))
            return "{}–{}".format(
                sections[0].numeric_label, sections[-1].numeric_label)
        # else:
        #     sections = sorted(
        #         self.sections.all(), key=lambda x: x.section_number)
        #     return "{}–{}".format(
        #         sections[0].label, sections[-1].label)

    class Meta:
        ordering = ['label']


@python_2_unicode_compatible
class Section(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    contents = models.TextField(blank=True)
    subpart = models.ForeignKey(Subpart, related_name="sections")

    panels = [
        FieldPanel('label'),
        FieldPanel('subpart'),
        FieldPanel('title'),
        FieldPanel('contents', classname="full"),
    ]

    def __str__(self):
        return "{} {}".format(self.label, self.title)

    class Meta:
        ordering = ['label']

    @property
    def numeric_label(self):
        part, number = self.label.split('-')[:2]
        if number.isdigit():
            return '\xa7\xa0{}.{}'.format(part, number)

    @property
    def section_number(self):
        part, number = self.label.split('-')[:2]
        return number

    @property
    def title_content(self):
        return self.title.replace(self.numeric_label, '')
