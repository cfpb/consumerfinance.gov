from functools import cached_property

from django import forms

from wagtail.core import blocks
from wagtail.core.blocks.struct_block import StructBlockAdapter
from wagtail.core.telepath import register

from v1.atomic_elements import organisms


class FigSection(blocks.StructBlock):
    header = blocks.TextBlock(label="Section header")
    section_id = blocks.TextBlock(
        required=False, help_text="Will be filled in automatically upon save."
    )
    content = organisms.FullWidthText()

    class Meta:
        icon = "edit"
        template = "_includes/organisms/fig-section.html"


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


class FigSubSection(FigSection):
    header = blocks.TextBlock(label="Subsection header")


class FigSub3Section(FigSection):
    header = blocks.TextBlock(label="Level 3 subsection header")
