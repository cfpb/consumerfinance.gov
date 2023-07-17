from django import forms
from django.utils.functional import cached_property

from wagtail import blocks
from wagtail.contrib.table_block.blocks import (
    TableBlock,
    TableInput,
    TableInputAdapter,
)
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.telepath import register

from v1.blocks import HeadingBlock


class RichTextTableInput(TableInput):
    @cached_property
    def media(self):
        media = super().media
        rich_text_media = forms.Media(
            js=["apps/admin/js/rich-text-table.js"],
        )
        return media + rich_text_media


class RichTextTableInputAdapter(TableInputAdapter):
    js_constructor = "v1.widgets.RichTextTableInput"


register(RichTextTableInputAdapter(), RichTextTableInput)


class AtomicTableBlock(TableBlock):
    @cached_property
    def field(self):
        widget = RichTextTableInput(table_options=self.table_options)
        return forms.CharField(widget=widget, **self.field_options)

    def to_python(self, value):
        new_value = super().to_python(value)
        if new_value:
            new_value["has_data"] = self.get_has_data(new_value)
        return new_value

    def get_has_data(self, value):
        has_data = False
        if value and "data" in value:
            first_row_index = (
                1 if value.get("first_row_is_table_header", None) else 0
            )
            first_col_index = (
                1 if value.get("first_col_is_header", None) else 0
            )

            for row in value["data"][first_row_index:]:
                for cell in row[first_col_index:]:
                    if cell:
                        has_data = True
                        break
                if has_data:
                    break
        return has_data

    def get_table_options(self, table_options=None):
        collected_table_options = super().get_table_options(
            table_options=table_options
        )
        collected_table_options["editor"] = "RichTextEditor"
        collected_table_options["outsideClickDeselects"] = False
        return collected_table_options

    class Meta:
        default = None
        icon = "table"
        template = "v1/includes/organisms/tables/atomic.html"
        label = "Table (Deprecated)"


class ContactUsRow(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock(features=["bold", "italic", "link"])


class ContactUsTable(blocks.StructBlock):
    heading = blocks.CharBlock()
    rows = blocks.ListBlock(ContactUsRow, collapsed=True, min_num=1)

    class Meta:
        icon = "table"
        template = "v1/includes/organisms/tables/contact-us.html"
        label = "Table (Contact Us)"


class ConsumerReportingCompanyTable(blocks.StructBlock):
    website = blocks.RichTextBlock(features=["bold", "italic", "link"])
    phone = blocks.RichTextBlock(features=["bold", "italic", "link"])
    mailing_address = blocks.RichTextBlock(features=["bold", "italic", "link"])

    class Meta:
        icon = "table"
        template = (
            "v1/includes/organisms/tables/consumer-reporting-company.html"
        )
        label = "Table (Consumer Reporting Company)"


class CaseDocketEventAttachment(blocks.StructBlock):
    id = blocks.CharBlock()
    title = blocks.CharBlock()
    document = DocumentChooserBlock(required=False)


class CaseDocketEvent(blocks.StructBlock):
    index = blocks.CharBlock()
    date_filed = blocks.DateBlock()
    document = DocumentChooserBlock(required=False)
    description = blocks.CharBlock()
    filed_by = blocks.CharBlock()
    attachments = blocks.ListBlock(
        CaseDocketEventAttachment, collapsed=True, default=[]
    )

    class Meta:
        label_format = "{index} - {description}"


class CaseDocketTable(blocks.StructBlock):
    events = blocks.ListBlock(CaseDocketEvent, collapsed=True, min_num=1)

    class Meta:
        icon = "table"
        template = "v1/includes/organisms/tables/case-docket.html"
        label = "Table (Case Docket)"
        unescape = False


class Table(blocks.StructBlock):
    heading = HeadingBlock(required=False)
    options = blocks.MultipleChoiceBlock(
        choices=[
            ("is_full_width", "Display the table at full width"),
            ("stack_on_mobile", "Stack the table columns on mobile"),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    data = TypedTableBlock(
        [
            ("text", blocks.CharBlock()),
            ("numeric", blocks.FloatBlock()),
            (
                "rich_text",
                blocks.RichTextBlock(
                    features=[
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "link",
                        "document-link",
                        "superscript",
                    ]
                ),
            ),
        ]
    )

    class Meta:
        icon = "table"
        template = "v1/includes/organisms/tables/base.html"
        unescape = False
