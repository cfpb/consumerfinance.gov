# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.html import strip_tags

from wagtail.wagtailadmin.edit_handlers import FieldPanel

from regulations3k import regdown


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
        return "Effective on {}".format(self.effective_date)

    class Meta:
        ordering = ['effective_date']
        default_related_name = 'version'


@python_2_unicode_compatible
class Subpart(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    version = models.ForeignKey(EffectiveVersion, related_name="subparts")

    BODY = 0000
    APPENDIX = 1000
    INTERPRETATION = 2000
    SUBPART_TYPE_CHOICES = (
        (BODY, 'Regulation Body'),
        (APPENDIX, 'Appendix'),
        (INTERPRETATION, 'Interpretation'),
    )
    subpart_type = models.IntegerField(
        choices=SUBPART_TYPE_CHOICES,
        default=BODY,
    )

    panels = [
        FieldPanel('label'),
        FieldPanel('title'),
        FieldPanel('subpart_type'),
        FieldPanel('version'),
    ]

    def __str__(self):
        return self.title

    @property
    def subpart_heading(self):
        """Keeping for now as possible hook into secondary nav"""
        return ''

    @property
    def section_range(self):
        if self.subpart_type != Subpart.BODY or not self.sections.exists():
            return ''

        sections = self.sections.all()
        return "{}–{}".format(
            sections[0].numeric_label, sections.reverse()[0].numeric_label)

    class Meta:
        ordering = ['subpart_type', 'label']


@python_2_unicode_compatible
class Section(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    contents = models.TextField(blank=True)
    subpart = models.ForeignKey(Subpart, related_name="sections")
    sortable_label = models.CharField(max_length=255)

    panels = [
        FieldPanel('label'),
        FieldPanel('subpart'),
        FieldPanel('title'),
        FieldPanel('contents', classname="full"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sortable_label']

    def extract_graphs(self):
        """Break out and store a section's paragraphs for indexing."""
        part = self.subpart.version.part
        extractor = regdown.extract_labeled_paragraph
        paragraph_ids = re.findall(r'[^{]*{(?P<label>[\w\-]+)}', self.contents)
        created = 0
        deleted = 0
        kept = 0
        exclude_from_deletion = []
        for pid in paragraph_ids:
            raw_graph = extractor(pid, self.contents, exact=True)
            re.sub(r'(See\([^\)]+\))', '', raw_graph)
            markup_graph = regdown.regdown(raw_graph)
            index_graph = strip_tags(markup_graph).strip()
            if index_graph:
                graph, cr = SectionParagraph.objects.get_or_create(
                    paragraph=index_graph,
                    paragraph_id=pid,
                    section=self)
                if cr:
                    created += 1
                else:
                    kept += 1
                exclude_from_deletion.append(graph.pk)
        to_delete = SectionParagraph.objects.filter(
            section__subpart__version__part=part,
            section__label=self.label).exclude(
            pk__in=exclude_from_deletion)
        deleted += to_delete.count()
        for graph in to_delete:
            graph.delete()
        return {
            'section': self.title,
            'created': created,
            'deleted': deleted,
            'kept': kept,
        }

    def save(self, **kwargs):
        self.sortable_label = '-'.join(sortable_label(self.label))
        super(Section, self).save(**kwargs)

    @cached_property
    def part(self):
        return self.subpart.version.part.part_number

    @property
    def section_number(self):
        return self.label

    @property
    def numeric_label(self):
        if self.label.isdigit():
            return '\xa7\xa0{}.{}'.format(self.part, int(self.label))
        else:
            return ''

    @property
    def title_content(self):
        if self.numeric_label:
            return self.title.replace(self.numeric_label, '').strip()
        else:
            return self.title


@python_2_unicode_compatible
class SectionParagraph(models.Model):
    """Provide storage for section paragraphs."""

    paragraph = models.TextField(blank=True)
    paragraph_id = models.CharField(max_length=255, blank=True)
    section = models.ForeignKey(Section, related_name="paragraphs")

    def __str__(self):
        return "Section {}-{} paragraph {}".format(
            self.section.part, self.section.label, self.paragraph_id)
