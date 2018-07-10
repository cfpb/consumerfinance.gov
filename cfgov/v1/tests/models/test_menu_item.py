from django.test import TestCase

from v1.models import MenuItem


class TestAccessibleLinks(TestCase):
    def test_aria_attributes_added_to_link_with_preceding_text(self):
        test_input = '<p>Text with <a href="/">link</a></p>'
        expected_output = (
            '<p><span aria-hidden="true">Text with </span>'+
            '<a aria-label="Text with link" href="/">link</a></p>'
        )
        self.assertEqual(
            MenuItem.accessible_links(test_input),
            expected_output
        )

    def test_aria_attributes_added_to_link_with_surrounding_text(self):
        test_input = '<p>Text with <a href="/">link</a> and following text</p>'
        expected_output = (
            '<p><span aria-hidden="true">Text with </span>' +
            '<a aria-label="Text with link and following text" ' +
            'href="/">link</a>' +
            '<span aria-hidden="true"> and following text</span></p>'
        )
        self.assertEqual(
            MenuItem.accessible_links(test_input),
            expected_output
        )

    def test_span_sibling_not_wrapped_in_span(self):
        test_input = (
            '<p><span>Text with </span><a href="/">link</a>' +
            ' and following text</p>'
        )
        expected_output = (
            '<p><span aria-hidden="true">Text with </span>' +
            '<a aria-label="Text with link and following text" ' +
            'href="/">link</a>' +
            '<span aria-hidden="true"> and following text</span></p>'
        )
        self.assertEqual(
            MenuItem.accessible_links(test_input),
            expected_output
        )

    def test_no_aria_attributes_added_to_link_without_accompanying_text(self):
        test_input = '<p><a href="/">Standalone link</a></p>'
        self.assertEqual(
            MenuItem.accessible_links(test_input),
            test_input
        )

    def test_no_aria_attributes_added_to_text_without_accompanying_link(self):
        test_input = '<p>Standalone text</p>'
        self.assertEqual(
            MenuItem.accessible_links(test_input),
            test_input
        )
