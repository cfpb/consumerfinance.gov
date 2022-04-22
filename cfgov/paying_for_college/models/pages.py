from wagtail.admin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField

from v1.atomic_elements import molecules, organisms
from v1.models import CFGOVPage


class PayingForCollegePage(CFGOVPage):
    """A base class for our suite of PFC pages."""

    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
        ],
        blank=True,
    )

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    class Meta:
        abstract = True

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["return_user"] = "iped" in request.GET and request.GET["iped"]
        return context


class PayingForCollegeContent(blocks.StreamBlock):
    """A base content block for PFC pages."""

    full_width_text = organisms.FullWidthText()
    info_unit_group = organisms.InfoUnitGroup()
    expandable_group = organisms.ExpandableGroup()
    expandable = organisms.Expandable()
    well = organisms.Well()
    raw_html_block = blocks.RawHTMLBlock(label="Raw HTML block")


class CollegeCostsPage(PayingForCollegePage):
    """Breaking down financial aid and loans for prospective students."""

    header = StreamField(
        [
            ("hero", molecules.Hero()),
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
        ],
        blank=True,
    )

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            # ObjectList(, heading='School and living situation'),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )
    content = StreamField(PayingForCollegeContent, blank=True)
    template = "paying-for-college/college-costs.html"


class RepayingStudentDebtPage(PayingForCollegePage):
    """A page to serve static subpages in the paying-for-college suite."""

    content = StreamField(PayingForCollegeContent, blank=True)
    template = "paying-for-college/repaying-student-debt.html"
