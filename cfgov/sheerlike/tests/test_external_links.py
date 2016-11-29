from mock import call, patch
from unittest import TestCase

from sheerlike.external_links import process_doc, process_external_links


class TestProcessDoc(TestCase):
    def test_applies_parse_links(self):
        with patch('sheerlike.external_links.parse_links') as parse_links:
            html = '<html><body><div>Hello</div></body></html>'
            process_doc(html)
            parse_links.assert_called_once_with(html)


class TestProcessExternalLinks(TestCase):
    doc = {
        'foo': [
            'a',
            'b',
            ['c', 'd', 'e'],
        ],
        'bar': {
            'x': 'f',
            'y': 'g',
            'z': ['h', 'i'],
        },
    }

    with patch('sheerlike.external_links.parse_links') as parse_links:
        process_external_links(doc)
        parse_links.assert_has_calls(
            list(map(call, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])),
            any_order=True
        )
