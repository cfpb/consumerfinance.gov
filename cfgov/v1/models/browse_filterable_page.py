from operator import attrgetter

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.db.models import Q

from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from . import base, molecules, organisms, ref
from .learn_page import AbstractFilterPage
from .. import forms
from ..util import filterable_context


class BrowseFilterablePage(base.CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
    ])
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterControls()),
    ])

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # General content tab
    content_panels = base.CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    sidefoot_panels = base.CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='SideFoot'),
        ObjectList(base.CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'browse-filterable/index.html'

    def add_page_js(self, js):
        super(BrowseFilterablePage, self).add_page_js(js)
        js['template'] += ['secondary-navigation.js']

    def get_context(self, request, *args, **kwargs):
        context = super(BrowseFilterablePage, self).get_context(request, *args, **kwargs)
        return filterable_context.get_context(self, request, context)

    def get_form_class(self):
        return forms.FilterableListForm

    def get_page_set(self, form, hostname):
        return filterable_context.get_page_set(self, form, hostname)


class EventArchivePage(BrowseFilterablePage):
    def get_form_class(self):
        return forms.EventArchiveFilterForm

    def get_template(self, request, *args, **kwargs):
        return BrowseFilterablePage.template


class NewsroomLandingPage(BrowseFilterablePage):
    def get_form_class(self):
        return forms.NewsroomFilterForm

    def get_template(self, request, *args, **kwargs):
        return BrowseFilterablePage.template
