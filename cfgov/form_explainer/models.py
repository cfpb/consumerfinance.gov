from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField

from form_explainer.blocks import Explainer
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class FormExplainerContent(StreamBlock):
    """Defines the StreamField blocks for FormExplainer page's content.
    Pages can have at most one Explainer block.
    """

    explainer = Explainer()
    well = organisms.Well()
    info_unit_group = organisms.InfoUnitGroup()
    full_width_text = organisms.FullWidthText()

    class Meta:
        block_counts = {
            "explainer": {"max_num": 1},
        }


class FormExplainerPage(CFGOVPage):
    header = StreamField(
        [
            ("hero", molecules.Hero()),
            ("text_introduction", molecules.TextIntroduction()),
        ],
        blank=True,
    )

    content = StreamField(
        FormExplainerContent,
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "form-explainer/index.html"
