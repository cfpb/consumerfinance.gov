from itertools import chain
from operator import attrgetter

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.db.models import Q

from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from .base import CFGOVPage
from .learn_page import AbstractFilterPage
from ..atomic_elements import molecules, organisms
from ..feeds import FilterableFeedPageMixin
from ..util.filterable_list import FilterableListMixin
from .. import blocks as v1_blocks


class BrowseFilterablePage(FilterableFeedPageMixin, FilterableListMixin, CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
    ])
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterControls()),
        ('feedback', v1_blocks.Feedback()),
    ])

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='SideFoot'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'browse-filterable/index.html'

    objects = PageManager()

    def add_page_js(self, js):
        super(BrowseFilterablePage, self).add_page_js(js)
        js['template'] += ['secondary-navigation.js']


class EventArchivePage(BrowseFilterablePage):
    template = 'browse-filterable/index.html'

    objects = PageManager()

    @staticmethod
    def get_form_class():
        from .. import forms
        return forms.EventArchiveFilterForm


class NewsroomLandingPage(BrowseFilterablePage):
    template = 'newsroom/index.html'

    objects = PageManager()

    @staticmethod
    def get_form_class():
        from .. import forms
        return forms.NewsroomFilterForm

    def get_page_set(self, form, hostname):
        get_blog = True
        only_blog = False
        for f in self.content:
            if 'filter_controls' in f.block_type and f.value['categories']['page_type'] == 'newsroom':
                categories = form.cleaned_data.get('categories', [])
                if categories:
                    if 'blog' not in categories:
                        get_blog = False
                    else:
                        if len(categories) == 1:
                            only_blog = True
        blog_q = Q()
        newsroom_q = Q()
        if not only_blog:
            newsroom_q = AbstractFilterPage.objects.child_of_q(self)
            newsroom_q &= form.generate_query()
        if get_blog:
            try:
                del form.cleaned_data['categories']
                blog = CFGOVPage.objects.get(slug='blog')
                blog_q = AbstractFilterPage.objects.child_of_q(blog)
                blog_q &= form.generate_query()
            except CFGOVPage.DoesNotExist:
                print 'Blog does not exist'

        return AbstractFilterPage.objects.live_shared(hostname).filter(newsroom_q | blog_q).distinct().order_by(
            '-date_published')
