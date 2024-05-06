from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField

from v1.atomic_elements import molecules, organisms
from v1.documents import (
    EnforcementActionFilterablePagesDocumentSearch,
    EventFilterablePagesDocumentSearch,
)
from v1.models.browse_page import AbstractBrowsePage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.filterable_page import AbstractFilterablePage
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


class BrowseFilterablePage(AbstractFilterablePage, AbstractBrowsePage):
    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
        ],
    )
    content = StreamField(
        BrowseFilterableContent,
        blank=True,
    )

    # General content tab
    content_panels = AbstractBrowsePage.content_panels + [
        FieldPanel("header"),
        FieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(
                AbstractFilterablePage.filtering_panels, heading="Filtering"
            ),
            ObjectList(AbstractBrowsePage.sidefoot_panels, heading="SideFoot"),
            ObjectList(
                AbstractBrowsePage.settings_panels,
                heading="Configuration",
            ),
        ]
    )

    template = "v1/browse-filterable/index.html"

    page_description = (
        "Left-hand navigation, no right-hand sidebar. Use if children should "
        "be searchable using standard search filters module."
    )

    subpage_types = ["DocumentDetailPage", "EventPage", "BrowsePage"]


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

    subpage_types = ["EnforcementActionPage"]


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


class NewsroomLandingPage(BrowseFilterablePage):
    template = "v1/newsroom/index.html"
    filterable_categories = ["Newsroom"]
    subpage_types = ["NewsroomPage"]
