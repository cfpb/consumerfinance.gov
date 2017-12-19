from django.test import TestCase, override_settings

from mock import call, patch

from sheerlike.external_links import process_external_links


@override_settings(AWS_STORAGE_BUCKET_NAME='foo.bucket')
class TestProcessExternalLinks(TestCase):
    def setUp(self):
        self.doc = {
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

    def test_applies_convert_http_image_links(self):
        url_mappings = [
            ('http://foo.bucket/', 'https://s3.amazonaws.com/foo.bucket/'),
        ]

        with patch(
            'sheerlike.external_links.convert_http_image_links',
            return_value='html'
        ) as convert:
            process_external_links(self.doc)
            convert.assert_has_calls(
                [
                    call(x, url_mappings)
                    for x in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
                ],
                any_order=True
            )

    def test_applies_parse_links(self):
        with patch('sheerlike.external_links.parse_links') as parse_links:
            process_external_links(self.doc)
            parse_links.assert_has_calls(
                list(map(call, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])),
                any_order=True
            )

    def test_converts_http_s3_link(self):
            doc = '<img src="http://foo.bucket/img.png"/>'
            self.assertEqual(
                process_external_links(doc),
                '<img src="https://s3.amazonaws.com/foo.bucket/img.png"/>'
            )
