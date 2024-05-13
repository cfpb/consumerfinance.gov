from functools import cached_property

from django import forms

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register

from v1.atomic_elements import molecules, organisms, schema


content_block_options = [
    ("content", blocks.RichTextBlock(icon="edit")),
    ("info_unit_group", organisms.InfoUnitGroup()),
    ("well", organisms.Well()),
    ("simple_chart", organisms.SimpleChart()),
    ("expandable_group", organisms.ExpandableGroup()),
    ("expandable", organisms.Expandable()),
    ("video_player", organisms.VideoPlayer()),
    ("raw_html_block", blocks.RawHTMLBlock(label="Raw HTML block")),
    ("notification", molecules.Notification()),
    ("faq_group", schema.FAQGroup()),
]


class FigDataPointsBlock(blocks.StaticBlock):
    class Meta:
        icon = "user"
        label = "FIG data points"
        admin_text = """
            The FIG data points are imported in the Data Points tab,
            and will be inserted in this place in the Wagtail page.
            """
        template = "filing_instruction_guide/data_points.html"


class FigSection(blocks.StructBlock):
    header = blocks.TextBlock(label="Section header (h2)")
    section_id = blocks.TextBlock(
        required=False, help_text="Will be filled in automatically upon save."
    )
    content = blocks.StreamBlock(
        content_block_options + [("data_points_block", FigDataPointsBlock())],
        block_counts={"data_points_block": {"max_num": 1}},
        required=False,
    )

    class Meta:
        icon = "edit"
        template = "filing_instruction_guide/section.html"


class FigSectionAdapter(StructBlockAdapter):
    js_constructor = "filing_instruction_guide.blocks.FigSection"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/fig-section-block.js"],
            css=structblock_media._css,
        )


register(FigSectionAdapter(), FigSection)


class FigSubsection(FigSection):
    header = blocks.TextBlock(label="Subsection header (h3)")
    content = blocks.StreamBlock(
        content_block_options,
        required=False,
    )


class FigLevel3Subsection(FigSection):
    header = blocks.TextBlock(label="Level 3 subsection header (h4)")
    content = blocks.StreamBlock(
        content_block_options,
        required=False,
    )
