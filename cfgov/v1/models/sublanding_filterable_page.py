from itertools import chain
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
from .feeds import FilterableFeedPageMixin


class SublandingFilterablePage(FilterableFeedPageMixin, base.CFGOVPage):
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

    def get_page_set(page, form, hostname):
        queries = {}
        selections = {}
        categories_cache = list(form.cleaned_data.get('categories', []))

        # Get filter selections for Blog and Report
        for f in page.content:
            if 'filter_controls' in f.block_type and f.value['categories']['page_type'] == 'activity-log':
                categories = form.cleaned_data.get('categories', [])
                selections = {'blog': False, 'research-reports': False}
                for category in selections.keys():
                    if not categories or category in categories:
                        selections[category] = True
                        if category in categories:
                            del categories[categories.index(category)]

        # Get Newsroom pages
        if not categories_cache or map(lambda x: x in [c[0] for c in ref.choices_for_page_type('newsroom')], categories):
            try:
                parent = CFGOVPage.objects.get(slug='newsroom')
                queries['newsroom'] = AbstractFilterPage.objects.child_of_q(parent) & form.generate_query()
            except CFGOVPage.DoesNotExist:
                print 'Newsroom does not exist'

        # Get Blog and Report pages if they were selected
        del form.cleaned_data['categories']
        for slug, is_selected in selections.iteritems():
            if is_selected:
                try:
                    parent = CFGOVPage.objects.get(slug=slug)
                    queries.update({slug: AbstractFilterPage.objects.child_of_q(parent) & form.generate_query()})
                except CFGOVPage.DoesNotExist:
                    print slug, 'does not exist'

        # AND all selected queries together
        final_q = reduce(lambda x,y: x|y, queries.values())

        return AbstractFilterPage.objects.live_shared(hostname).filter(final_q).distinct().order_by('-date_published')


    def get_form_class(self):
        return forms.ActivityLogFilterForm
