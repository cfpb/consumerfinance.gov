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

from .base import CFGOVPage
from .learn_page import AbstractFilterPage
from .. import blocks as v1_blocks
from ..atomic_elements import molecules, organisms
from ..feeds import FilterableFeedPageMixin
from ..util.ref import choices_for_page_type
from ..util.filterable_list import FilterableListMixin


class SublandingFilterablePage(FilterableFeedPageMixin, FilterableListMixin, CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
    ], blank=True)
    content = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterControls()),
        ('featured_content', molecules.FeaturedContent()),
        ('feedback', v1_blocks.Feedback()),
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


class ActivityLogPage(SublandingFilterablePage):
    template = 'activity-log/index.html'


    @staticmethod
    def get_form_class():
        from .. import forms
        return forms.ActivityLogFilterForm


    def per_page_limit(self):
        return 100


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
                for selection, is_selected in selections.iteritems():
                    if is_selected and selection in categories:
                        del categories[categories.index(selection)]

        # Get Newsroom pages
        if not categories_cache or map(lambda x: x in [c[0] for c in choices_for_page_type('newsroom')], categories):
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
