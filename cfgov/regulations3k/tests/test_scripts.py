# -*- coding: utf-8 -*-
from unittest import mock

from django.test import TestCase

from regulations3k.models import Section
from regulations3k.scripts.insert_section_links import (
    REG_BASE, SECTION_RE, get_url, insert_links, insert_section_links, run
)


class LinkScriptTestCase(TestCase):

    fixtures = ['tree_limb']

    def test_bad_part_number_is_skipped(self):
        bad_ref = '99.5(d)(1)'
        test_url = get_url(bad_ref)
        self.assertIs(test_url, None)

    def test_part_number_not_in_allowlist(self):
        bad_ref = '1017.5(d)(1)'
        test_url = get_url(bad_ref)
        self.assertIs(test_url, None)

    def test_section_with_paragraph_ids(self):
        ref_with_id = '1002.1(a)'
        test_url = get_url(ref_with_id)
        self.assertEqual(test_url, REG_BASE.format('1002/1') + '#a')

    def test_section_no_paragraph_ids(self):
        no_ids_ref = '1002.1'
        test_url = get_url(no_ids_ref)
        self.assertEqual(test_url, REG_BASE.format('1002/1'))

    def test_section_blank_paragraph_ids(self):
        no_ids_ref = '1002.1()'
        test_url = get_url(no_ids_ref)
        self.assertEqual(test_url, REG_BASE.format('1002/1'))

    def test_insert_section_links_no_links_found(self):
        linkless_regdown = 'Regdown with no links.'
        test_result = insert_section_links(linkless_regdown)
        self.assertIsNone(test_result)

    def test_section_detection(self):
        """Ensure content containing a 'Section' reference is detected."""
        good_ref = 'Regdown with a reference to Section 1002.5(d)(1) included.'
        self.assertEqual(SECTION_RE.findall(good_ref)[0], '1002.5(d)(1)')

    def test_insert_section_links(self):
        """Ensure content with section sign becomes regs3k relative link."""
        test_regdown = (
            'Regdown with a linkable section § 1002.2(a).')
        test_result = insert_section_links(test_regdown)
        self.assertIn(REG_BASE.format('1002'), test_result)

    @mock.patch(
        'regulations3k.scripts.insert_section_links.get_url')
    def test_run_with_section(self, mock_get_url):
        mock_get_url.return_value = '/mock_relative/url/'
        run('1002')
        self.assertEqual(mock_get_url.call_count, 97)  # 97 refs in fixture

    @mock.patch(
        'regulations3k.scripts.insert_section_links.insert_section_links')
    def test_run_no_args(self, mock_inserter):
        """Check that passing no args will process all test regs."""
        mock_inserter.return_value = 'linked Regdown'
        run()
        self.assertEqual(mock_inserter.call_count, 4)  # 4 regs in fixture

    @mock.patch(
        'regulations3k.scripts.insert_section_links.insert_links')
    def test_run_with_args(self, mock_inserter):
        run('1002')
        self.assertTrue(mock_inserter.called_with, '1002')

    def test_insert_links_skips_processed_file(self):
        regdown_with_link = (
            'Regdown with a linked section <a data-linktag="0" '
            'href="/policy-compliance/rulemaking/regulations/1002/2/#a">'
            '\N{SECTION SIGN} 1002.2(a)</a>.')
        section = Section.objects.get(pk=1)  # Section 1002.4 in fixture
        section.contents = regdown_with_link
        section.save()
        insert_links('1002')
        self.assertEqual(section.contents, regdown_with_link)
