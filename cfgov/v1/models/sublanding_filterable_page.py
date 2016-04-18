from operator import attrgetter

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.db.models import Q

from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from . import base, molecules, organisms, ref
from .learn_page import AbstractFilterPage
from .. import forms
from ..util import filterable_context

from .base import CFGOVPage


class SublandingFilterablePage(base.CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
    ], blank=True)
    content = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterControls()),
        ('featured_content', molecules.FeaturedContent()),
    ])

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'sublanding-page/index.html'

    def get_context(self, request, *args, **kwargs):
        context = super(SublandingFilterablePage, self).get_context(request, *args, **kwargs)
        return filterable_context.get_context(self, request, context)

    def get_form_class(self):
        return forms.FilterableListForm

    def get_page_set(self, form, hostname):
        return filterable_context.get_page_set(self, form, hostname)


class ActivityLogPage(SublandingFilterablePage):
    template = 'activity-log/index.html'

    def get_form_class(self):
        return forms.ActivityLogFilterForm
