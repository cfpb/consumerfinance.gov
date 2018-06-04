from __future__ import absolute_import, unicode_literals

import re
from collections import OrderedDict
from functools import partial

from django.db import models
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils.functional import cached_property

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager

# Our RegDownTextField field doesn't generate a good widget yet
# from regulations3k.models.fields import RegDownTextField
from ask_cfpb.models.pages import SecondaryNavigationJSMixin
from regulations3k.models import Part, Section, sortable_label  # , Subpart
from regulations3k.regdown import regdown
from regulations3k.resolver import get_contents_resolver, get_url_resolver
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

    @cached_property
    def section_query(self):
        """ Query set for Sections in this regulation's effective version """
        return Section.objects.filter(
            subpart__version=self.regulation.effective_version,
        )

    @cached_property
    def sorted_sections(self):
        """ Sort all sections within our section_query on sortable_label """
        return sorted(self.section_query.all(),
                      key=lambda s: sortable_label(s.label))

    def get_context(self, request, *args, **kwargs):
        context = super(CFGOVPage, self).get_context(request, *args, **kwargs)
        context.update({
            'get_secondary_nav_items': get_reg_nav_items,
            'regulation': self.regulation,
            'section': None,
        })
        return context

    @route(r'^(?P<section>[0-9A-Za-z-]+)/$', name="section")
    def section_page(self, request, section):
        section_label = "{}-{}".format(
            self.regulation.part_number, section)

        section = self.section_query.get(label=section_label)
        current_index = self.sorted_sections.index(section)
        context = self.get_context(request)

        content = regdown(
            section.contents,
            url_resolver=get_url_resolver(self),
            contents_resolver=get_contents_resolver(self),
            render_block_reference=partial(self.render_interp, context)
        )

        context.update({
            'version': self.regulation.effective_version,
            'content': content,
            'get_secondary_nav_items': get_reg_nav_items,
            'next_section': get_next_section(
                self.sorted_sections, current_index),
            'previous_section': get_previous_section(
                self.sorted_sections, current_index),
            'section': section,
        })

        return TemplateResponse(
            request,
            self.template,
            context)

    def render_interp(self, context, raw_contents, **kwargs):
        template = get_template('regulations3k/inline_interps.html')

        # Extract the title from the raw regdown
        section_title_match = re.search(
            r'#+\s?(?P<section_title>.*)\s',
            raw_contents
        )
        if section_title_match is not None:
            context.update({
                'section_title': section_title_match.group(1)
            })
            span = section_title_match.span()
            raw_contents = raw_contents[:span[0]] + raw_contents[span[1]:]

        context.update({'contents': regdown(raw_contents)})
        context.update(kwargs)

        return template.render(context)


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


def get_reg_nav_items(request, current_page):
    url_bits = [bit for bit in request.url.split('/') if bit]
    current_label = url_bits[-1]
    current_part = current_page.regulation.part_number
    subpart_list = set(
        [section.subpart for section in current_page.sorted_sections])
    subpart_dict = OrderedDict(
        [(subpart, None) for subpart in subpart_list]
    )
    for subpart in subpart_dict:
        sorted_sections = sorted(
            subpart.sections.all(),
            key=lambda s: sortable_label(s.label))
        subpart_dict[subpart] = [
            {
                'title': section.title,
                'url': current_page.url + current_page.reverse_subpage(
                    'section',
                    args=([section.label.partition('-')[-1]])
                ),
                'active': section.label == '{}-{}'.format(
                    current_part,
                    current_label),
                'expanded': True,
                'section': section,
            }
            for section in sorted_sections
        ]
    return subpart_dict, False
