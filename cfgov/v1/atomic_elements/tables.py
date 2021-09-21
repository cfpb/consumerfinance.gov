import json

from django import forms
from django.utils.functional import cached_property

from wagtail.contrib.table_block.blocks import (
    TableBlock, TableInput, TableInputAdapter
)
from wagtail.core.rich_text import expand_db_html
from wagtail.core.telepath import register

from jinja2 import Markup


class RichTextTableInput(TableInput):
    @cached_property
    def media(self):
        media = super().media
        rich_text_media = forms.Media(
            js=[
                'js/admin/rich-text-table.js',
            ],
        )
        return media + rich_text_media


class RichTextTableInputAdapter(TableInputAdapter):
    js_constructor = 'wagtail.widgets.TableInput'


register(RichTextTableInputAdapter(), RichTextTableInput)


class AtomicTableBlock(TableBlock):
    @cached_property
    def field(self):
        widget = RichTextTableInput(table_options=self.table_options)
        return forms.CharField(widget=widget, **self.field_options)

    def to_python(self, value):
        new_value = super(AtomicTableBlock, self).to_python(value)
        if new_value:
            new_value['has_data'] = self.get_has_data(new_value)
        return new_value

    def get_has_data(self, value):
        has_data = False
        if value and 'data' in value:
            first_row_index = 1 if value.get('first_row_is_table_header',
                                             None) else 0
            first_col_index = 1 if value.get('first_col_is_header',
                                             None) else 0

            for row in value['data'][first_row_index:]:
                for cell in row[first_col_index:]:
                    if cell:
                        has_data = True
                        break
        return has_data

    def get_table_options(self, table_options=None):
        collected_table_options = super().get_table_options(
            table_options=table_options
        )
        collected_table_options['editor'] = 'RichTextEditor'
        return collected_table_options

    class Meta:
        default = None
        icon = 'table'
        template = '_includes/organisms/table.html'
        label = 'Table'
