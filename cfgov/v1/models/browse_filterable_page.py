from django.db import models

from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from .base import CFGOVPage
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

    def get_filter_parent(self):
        """ The Newsroom never filters results by a parent page """
        return None
