import json

from django.test import TestCase

from wagtail.core.models import Site
from wagtail.tests.testapp.models import SimplePage

from v1.atomic_elements.organisms import AtomicTableBlock, RichTextTableInput


class TestRichTextTableInput(TestCase):
    def test_json_dict_apply_none(self):
        self.assertEqual(
            RichTextTableInput.json_dict_apply('null', lambda x: x),
            'null'
        )

    def test_json_dict_apply_modifies_each_cell(self):
        value = {
            'foo': 'bar',
            'data': [
                ['a', 'b', None],
                [],
                ['d', 'e', ''],
            ]
        }

        applied_value = RichTextTableInput.json_dict_apply(
            json.dumps(value),
            lambda x: 2 * x
        )

        self.assertEqual(
            json.loads(applied_value),
            {
                'foo': 'bar',
                'data': [
                    ['aa', 'bb', None],
                    [],
                    ['dd', 'ee', ''],
                ]
            }
        )


class TestAtomicTableBlock(TestCase):
    def test_render_with_data(self):
        value = {
            'data': [['Header 1', 'Header 2'], ['1', '2']]
        }
        block = AtomicTableBlock()
        result = block.render(value)
        self.assertIn('<table', result)

    def test_render_rich_text_page_links_expanded(self):
        page = SimplePage(title='title', slug='slug', content='content')
        default_site = Site.objects.get(is_default_site=True)
        default_site.root_page.add_child(instance=page)

        value = {
            'data': [[
                '<a linktype="page" id="{}">'.format(page.pk)
            ]],
        }
        block = AtomicTableBlock()
        result = block.render(value)
        self.assertIn('href="/slug/"', result)

    def test_render_header_with_unicode_characters(self):
        value = {
            'data': [[u'H\xebader 1', 'Header 2'], ['1', '2']],
            'first_row_is_table_header': True,
            'is_stacked': True,
        }
        block = AtomicTableBlock()
        result = block.render(value)
        self.assertIn(u'H\xebader', result)
