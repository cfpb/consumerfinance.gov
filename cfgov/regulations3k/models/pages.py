from __future__ import absolute_import, unicode_literals

from django.db import models
from django.template.response import TemplateResponse
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager

from regulations3k.models.fields import RegDownTextField
from regulations3k.models import Part, Subpart
from v1.models import CFGOVPage, CFGOVPageManager
from v1.atomic_elements import molecules
from v1.util.util import get_secondary_nav_items


class RegulationLandingPage(CFGOVPage):
    """landing page for eregs"""
    objects = CFGOVPageManager()

    def get_template(self, request):
        return 'regulations3k/base.html'


class RegulationPage(RoutablePageMixin, CFGOVPage):
    """A routable page for serving an eregulations page by subpart ID"""

    objects = PageManager()

    def get_template(self, request):
        return 'browse-basic/index.html'

    regdown = RegDownTextField(default='regdown text')

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
        FieldPanel('regdown', classname="full"),
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
        context.update({'get_secondary_nav_items': get_secondary_nav_items})
        context.update({'regulation': self.regulation})
        return context

    @route(r'^(?P<part_label>[0-9]+)/(?P<section_label>[0-9A-za-z-]+)$')
    def part_section_page(self, request, part_label, section_label):
        part = Part.objects.get(part_number=part_label)
        subpart = Subpart.objects.get(label=section_label)
        context = self.get_context(request)
        context['part'] = part.get_effective_version()
        context['subpart'] = subpart.get_effective_version()
        return TemplateResponse(
            request,
            self.get_template(request),
            context)
