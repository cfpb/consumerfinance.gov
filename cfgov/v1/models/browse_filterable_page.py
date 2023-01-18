from django.db import models

from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField

from v1.atomic_elements import molecules, organisms
from v1.documents import (
    EnforcementActionFilterablePagesDocumentSearch,
    EventFilterablePagesDocumentSearch,
)
from v1.models.base import CFGOVPage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.filterable_list_mixins import (
    CategoryFilterableMixin,
    FilterableListMixin,
)
from v1.models.learn_page import EventPage


class BrowseFilterableContent(StreamBlock):
    """Defines the StreamField blocks for BrowseFilterablePage content.

    Pages can have at most one filterable list.
    """

    full_width_text = organisms.FullWidthText()
    filter_controls = organisms.FilterableList()

    class Meta:
        block_counts = {
            "filter_controls": {"max_num": 1},
        }


class BrowseFilterablePage(FilterableListMixin, CFGOVPage):
    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
        ]
    )
    content = StreamField(BrowseFilterableContent)

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("content"),
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel("secondary_nav_exclude_sibling_pages"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(sidefoot_panels, heading="SideFoot"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "v1/browse-filterable/index.html"

    page_description = (
        "Left-hand navigation, no right-hand sidebar. Use if children should "
        "be searchable using standard search filters module."
    )

    @property
    def page_js(self):
        return super().page_js + ["secondary-navigation.js"]


class EnforcementActionsFilterPage(BrowseFilterablePage):
    template = "v1/browse-filterable/index.html"

    @staticmethod
    def get_form_class():
        from .. import forms

        return forms.EnforcementActionsFilterForm

    @staticmethod
    def get_model_class():
        return EnforcementActionPage

    @staticmethod
    def get_search_class():
        return EnforcementActionFilterablePagesDocumentSearch


class EventArchivePage(BrowseFilterablePage):
    template = "v1/browse-filterable/index.html"

    @staticmethod
    def get_model_class():
        return EventPage

    @staticmethod
    def get_form_class():
        from .. import forms

        return forms.EventArchiveFilterForm

    @staticmethod
    def get_search_class():
        return EventFilterablePagesDocumentSearch


class NewsroomLandingPage(CategoryFilterableMixin, BrowseFilterablePage):
    template = "v1/newsroom/index.html"
    filterable_categories = ["Newsroom"]
