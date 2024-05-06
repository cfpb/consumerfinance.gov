from wagtail import blocks
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.fields import StreamField

from v1.atomic_elements import molecules, organisms
from v1.models import CFGOVPage


class CollegeCostsPage(CFGOVPage):
    """Breaking down financial aid and loans for prospective students."""

    header = StreamField(
        [
            ("hero", molecules.Hero()),
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
        ],
        blank=True,
    )

    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("expandable", organisms.Expandable()),
            ("well", organisms.Well()),
            ("raw_html_block", blocks.RawHTMLBlock(label="Raw HTML block")),
        ],
        blank=True,
    )

    content_panels = CFGOVPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("content"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "paying-for-college/college-costs.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["return_user"] = "iped" in request.GET and request.GET["iped"]
        return context
