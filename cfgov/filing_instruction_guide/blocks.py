from functools import cached_property

from django import forms

from wagtail.core import blocks
from wagtail.core.blocks.struct_block import StructBlockAdapter
from wagtail.core.telepath import register

from v1.atomic_elements import organisms, schema


class FigSection(blocks.StructBlock):
    header = blocks.TextBlock(label="Section header (h2)")
    section_id = blocks.TextBlock(
        required=False, help_text="Will be filled in automatically upon save."
    )
    content = blocks.StreamBlock(
        [
            ("content", blocks.RichTextBlock(icon="edit")),
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("well", organisms.Well()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("simple_chart", organisms.SimpleChart()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("expandable", organisms.Expandable()),
            ("video_player", organisms.VideoPlayer()),
            ("snippet_list", organisms.ResourceList()),
            ("raw_html_block", blocks.RawHTMLBlock(label="Raw HTML block")),
            ("faq_group", schema.FAQGroup()),
        ],
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


class FigLevel3Subsection(FigSection):
    header = blocks.TextBlock(label="Level 3 subsection header (h4)")
