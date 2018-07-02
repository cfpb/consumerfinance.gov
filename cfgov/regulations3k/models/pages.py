from __future__ import absolute_import, unicode_literals

import re
from collections import OrderedDict
from functools import partial

from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
from django.utils.text import Truncator
from haystack.query import SearchQuerySet

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager

from ask_cfpb.models.pages import SecondaryNavigationJSMixin
from regulations3k.models import Part, Section, SectionParagraph
from regulations3k.parser.integer_conversion import LETTER_CODES
from regulations3k.regdown import regdown
from regulations3k.resolver import get_contents_resolver, get_url_resolver
from v1.atomic_elements import molecules
from v1.models import CFGOVPage, CFGOVPageManager


class RegulationsSearchPage(RoutablePageMixin, CFGOVPage):
    """A page for the custom search interface for regulations."""

    objects = PageManager()

    parent_page_types = ['regulations3k.RegulationLandingPage']
    subpage_types = []
    results = {}
    content_panels = CFGOVPage.content_panels
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    def get_template(self, request, partial=False):
        template = 'regulations3k/search-regulations.html'
        if partial:
            template = 'regulations3k/search-regulations-results.html'
        return template

    @route(r'^results/')
    def regulation_results_page(self, request):
        all_regs = Part.objects.order_by('part_number')
        regs = []
        order = request.GET.get('order', '')
        sqs = SearchQuerySet()
        if 'regs' in request.GET and request.GET.get('regs'):
            regs = request.GET.getlist('regs')
        search_query = request.GET.get('q', '')  # haystack cleans this string
        sqs = SearchQuerySet()
        if search_query:
            sqs = sqs.filter(content=search_query)
        if len(regs) == 1:
            sqs = sqs.filter(part=regs[0])
        elif regs:
            sqs = sqs.filter(part__in=regs)
        if order == 'regulation':
            sqs = sqs.order_by('part', 'section_order')
        sqs = sqs.models(SectionParagraph)
        payload = {
            'search_query': search_query,
            'results': [],
            'total_results': sqs.count(),
            'regs': regs,
            'all_regs': [{
                'name': "Regulation {}".format(reg.letter_code),
                'id': reg.part_number,
                'num_results': sqs.filter(part=reg.part_number).count(),
                'selected': reg.part_number in regs}
                for reg in all_regs
            ]
        }
        for hit in sqs:
            letter_code = LETTER_CODES.get(hit.part)
            snippet = Truncator(hit.text).words(50, truncate=' ...')
            hit_payload = {
                'id': hit.paragraph_id,
                'reg': 'Regulation {}'.format(letter_code),
                'label': hit.title,
                'snippet': snippet,
                'url': "/regulations/{}/{}/#{}".format(
                    hit.part, hit.section_label, hit.paragraph_id),
            }
            payload['results'].append(hit_payload)
        self.results = payload

        context = self.get_context(request)
        num_results = validate_num_results(request)
        paginator = Paginator(payload['results'], num_results)
        page_number = validate_page_number(request, paginator)
        paginated_page = paginator.page(page_number)
        context.update({
            'paginator': paginator,
            'current_page': page_number,
            'num_results': num_results,
            'order': order,
            'results': paginated_page,
        })

        return TemplateResponse(
            request,
            self.get_template(request, 'partial' in request.GET),
            context)


class RegulationLandingPage(CFGOVPage):
    """Landing page for eregs."""

    objects = CFGOVPageManager()
    subpage_types = ['regulations3k.RegulationPage', 'RegulationsSearchPage']
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
    """A routable page for serving an eregulations page by Section ID."""

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
        """Query set for Sections in this regulation's effective version."""
        return Section.objects.filter(
            subpart__version=self.regulation.effective_version,
        )

    @cached_property
    def sections(self):
        return list(self.section_query.all())

    def get_context(self, request, *args, **kwargs):
        context = super(CFGOVPage, self).get_context(request, *args, **kwargs)
        context.update({
            'get_secondary_nav_items': get_reg_nav_items,
            'regulation': self.regulation,
            'section': None,
            'breadcrumb_items': self.get_breadcrumbs(request)
        })
        return context

    def get_breadcrumbs(self, request, section=None):
        landing_page = self.get_parent()
        crumbs = [{
            'href': landing_page.url,
            'title': landing_page.title,
        }]

        if section is not None:
            crumbs = crumbs + [
                {
                    'href': self.url,
                    'title': str(section.subpart.version.part),
                },
                {
                    'title': section.subpart.title,
                },
            ]

        return crumbs

    @route(r'^(?P<section_label>[0-9A-Za-z-]+)/$', name="section")
    def section_page(self, request, section_label):
        section = self.section_query.get(label=section_label)
        current_index = self.sections.index(section)
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
                self.sections, current_index),
            'previous_section': get_previous_section(
                self.sections, current_index),
            'section': section,
            'breadcrumb_items': self.get_breadcrumbs(request, section),
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
    url_bits = [bit for bit in request.path.split('/') if bit]
    current_label = url_bits[-1]
    sections = current_page.sections
    subpart_dict = OrderedDict()

    for section in sections:
        # If the section's subpart isn't in the subpart dict yet, add it
        if section.subpart not in subpart_dict:
            subpart_dict[section.subpart] = {
                'sections': [],
                'expanded': False
            }

        # Create the section dictionary for navigation
        section_dict = {
            'title': section.title,
            'url': current_page.url + current_page.reverse_subpage(
                'section',
                args=([section.label])
            ),
            'active': section.label == current_label,
            'expanded': True,
            'section': section,
        }

        # Add it to the subpart
        subpart_dict[section.subpart]['sections'].append(
            section_dict
        )

        # Set the subpart to active if the section is active
        if section_dict['active']:
            subpart_dict[section.subpart]['expanded'] = True

    return subpart_dict, False


def validate_num_results(request):
    """
    A utility for parsing the requested number of results per page.

    This should catch an invalid number of results and always return
    a valid number of results, defaulting to 25.
    """
    raw_results = request.GET.get('results')
    if raw_results in ['50', '100']:
        return int(raw_results)
    else:
        return 25


def validate_page_number(request, paginator):
    """
    A utility for parsing a pagination request.

    This should catch invalid page numbers and always return
    a valid page number, defaulting to 1.
    """
    raw_page = request.GET.get('page', 1)
    try:
        page_number = int(raw_page)
    except ValueError:
        page_number = 1
    try:
        paginator.page(page_number)
    except InvalidPage:
        page_number = 1
    return page_number
