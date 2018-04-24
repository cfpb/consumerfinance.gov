from __future__ import absolute_import, unicode_literals

import re

from django.db import models
from django.template.response import TemplateResponse
from django.template.loader import get_template

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager

from regulations3k.models import Part, Section  # , Subpart
from regulations3k.regdown import regdown
from regulations3k.resolver import get_contents_resolver

# Our RegDownTextField field doesn't generate a good widget yet
# from regulations3k.models.fields import RegDownTextField
from ask_cfpb.models.pages import SecondaryNavigationJSMixin
from v1.atomic_elements import molecules
from v1.models import CFGOVPage, CFGOVPageManager


class RegulationLandingPage(CFGOVPage):
    """landing page for eregs"""
    objects = CFGOVPageManager()
    subpage_types = ['regulations3k.RegulationPage']
    regs = Part.objects.order_by('part_number')

    def get_context(self, request, *args, **kwargs):
        context = super(CFGOVPage, self).get_context(request, *args, **kwargs)
        context.update({
            'get_secondary_nav_items': get_reg_nav_items,
            'regs': self.regs,
        })
        return context

    def get_template(self, request):
        return 'regulations3k/base.html'


class RegulationPage(RoutablePageMixin, SecondaryNavigationJSMixin, CFGOVPage):
    """A routable page for serving an eregulations page by Section ID"""

    objects = PageManager()
    parent_page_types = ['regulations3k.RegulationLandingPage']
    subpage_types = []

    template = 'regulations3k/browse-regulation.html'

    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([], null=True)
    regulation = models.ForeignKey(
        Part,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='eregs3k_page')

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        FieldPanel('regulation', Part),
    ]

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    def get_context(self, request, *args, **kwargs):
        context = super(CFGOVPage, self).get_context(request, *args, **kwargs)
        context.update({
            'get_secondary_nav_items': get_reg_nav_items,
            'regulation': self.regulation,
            'section': None,
        })
        return context

    @route(r'^(?P<section>[0-9A-Za-z-]+)/$')
    def section_page(self, request, section):
        section_label = "{}-{}".format(
            self.regulation.part_number, section)
        section = Section.objects.filter(
            subpart__version=self.regulation.effective_version,
        ).get(label=section_label)
        content = regdown(
            section.contents,
            contents_resolver=get_contents_resolver(section),
            block_reference_template=get_template(
                'regulations3k/inline_interps.html'
            )
        )
        sibling_sections = sorted_section_nav_list(
            self.regulation.effective_version)
        current_index = sibling_sections.index(section)
        context = self.get_context(request)
        context.update({
            'version': self.regulation.effective_version,
            'content': content,
            'get_secondary_nav_items': get_reg_nav_items,
            'next_section': get_next_section(
                sibling_sections, current_index),
            'previous_section': get_previous_section(
                sibling_sections, current_index),
            'section': section,
        })

        return TemplateResponse(
            request,
            self.template,
            context)


def get_next_section(section_list, current_index):
    if current_index == len(section_list) - 1:
        return None
    else:
        return section_list[current_index + 1]


def get_previous_section(section_list, current_index):
    if current_index == 0:
        return None
    else:
        return section_list[current_index - 1]


def sorted_section_nav_list(version):
    numeric_check = re.compile('\d{4}\-(\d{1,2})')
    section_query = Section.objects.filter(
        subpart__version=version
    )
    numeric_sections = [sect for sect in section_query
                        if re.match(numeric_check, sect.label)]
    numeric_sorted = sorted(
        numeric_sections, key=lambda x: int(x.section_number))
    alpha_sorted = sorted(
        [sect for sect in section_query
         if sect not in numeric_sections], key=lambda x: x.title)
    return numeric_sorted + alpha_sorted


def get_reg_nav_items(request, current_page):
    version = current_page.regulation.effective_version
    url_bits = [bit for bit in request.url.split('/') if bit]
    current_label = url_bits[-1]
    current_part = current_page.regulation.part_number
    return [
        {
            'title': gathered_section.title,
            'url': '/eregulations3k/{}/{}/'.format(
                current_part,
                gathered_section.label.partition('-')[-1]),
            'active': gathered_section.label == '{}-{}'.format(
                current_part,
                current_label),
            'expanded': True,
            'section': gathered_section,
        }
        for gathered_section
        in sorted_section_nav_list(version)
    ], True
