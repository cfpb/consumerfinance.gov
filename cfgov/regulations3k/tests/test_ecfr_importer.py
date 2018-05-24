# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from django.conf import settings
from django.test import TestCase as DjangoTestCase

# from bs4 import BeautifulSoup as bS
import mock
# import markdown
# from regulations3k.regdown import extract_labeled_paragraph, regdown
from regulations3k.models import EffectiveVersion, Part, Subpart
from regulations3k.scripts.ecfr_importer import ecfr_to_regdown, run
from regulations3k.scripts.patterns import IdLevelState
from regulations3k.scripts.roman import int_to_roman, roman_to_int
from requests import Response


class ImporterTestCase(DjangoTestCase):

    fixtures = ['test_parts.json']  # fixture has XML for regs 1 and 1005
    xml_fixture = "{}/regulations3k/fixtures/graftest.xml".format(
        settings.PROJECT_ROOT)

    @mock.patch(
        'regulations3k.scripts.ecfr_importer.requests.get')
    def test_parser_good_request(self, mock_get):
        part_number = '1'
        with open(self.xml_fixture, 'r') as f:
            test_xml = f.read()
        mock_response = mock.Mock(
            Response, reason='OK', text=test_xml, encoding='utf-8')
        mock_get.return_value = mock_response
        ecfr_to_regdown(part_number)
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch('regulations3k.scripts.ecfr_importer.requests.get')
    def test_bad_parser_request_returns_none(self, mock_get):
        mock_response = mock.Mock(
            Response,
            reason='REQUESTS FOR HUMANS MY EYE',
            status_code='404')
        mock_get.return_value = mock_response
        self.assertIs(ecfr_to_regdown('1'), None)
        self.assertEqual(mock_get.call_count, 1)

    def test_nonexistent_part_number(self):
        part_number = '9999'
        self.assertIs(
            ecfr_to_regdown(part_number, file_path=self.xml_fixture), None)

    def test_part_parser_use_existing(self):
        part_number = '1003'
        ecfr_to_regdown(part_number, file_path=self.xml_fixture)
        self.assertEqual(Part.objects.filter(
            part_number=part_number).count(), 1)
        self.assertEqual(Subpart.objects.count(), 3)

    def test_part_parser_create_new(self):
        part_number = '1'
        ecfr_to_regdown(part_number, file_path=self.xml_fixture)
        self.assertEqual(Part.objects.filter(
            part_number=part_number).count(), 1)
        self.assertEqual(Subpart.objects.count(), 3)

    def test_part_created(self):
        ecfr_to_regdown('1', file_path=self.xml_fixture)
        self.assertEqual(Part.objects.filter(part_number='1').count(), 1)
        self.assertEqual(EffectiveVersion.objects.count(), 1)

    def test_bad_file_path_returns_none(self):
        self.assertIs(ecfr_to_regdown('1', file_path='fake_file_path'), None)
        self.assertEqual(Part.objects.filter(part_number='1').count(), 0)

    @mock.patch('regulations3k.scripts.ecfr_importer.ecfr_to_regdown')
    def test_run_with_one_arg_calls_importer(self, mock_importer):
        run('1')
        self.assertEqual(mock_importer.call_count, 1)

    def test_run_works_with_local_file(self):
        run('1', self.xml_fixture)
        self.assertEqual(Part.objects.filter(part_number='1').count(), 1)

    def test_run_importer_bad_args(self):
        with self.assertRaises(SystemExit):
            run()


class PatternsTestCase(unittest.TestCase):

    levelstate = IdLevelState()

    def test_level_1_surf(self):
        self.levelstate.current_id = 'a'
        self.levelstate.next_token = 'b'
        self.assertEqual(self.levelstate.next_id(), 'b')
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), 'b')

    def test_level_1_dive(self):
        self.levelstate.current_id = 'b'
        self.levelstate.next_token = '1'
        self.assertEqual(self.levelstate.next_id(), 'b-1')
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), '1')

    def test_level_2_surf(self):
        self.levelstate.current_id = 'a-1'
        self.levelstate.next_token = '2'
        self.assertEqual(self.levelstate.next_id(), 'a-2')
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), '2')

    def test_level_2_dive(self):
        self.levelstate.current_id = 'e-3'
        self.levelstate.next_token = 'i'
        self.assertEqual(self.levelstate.next_id(), 'e-3-i')
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), 'i')

    def test_level_2_rise(self):
        self.levelstate.current_id = 'e-3'
        self.levelstate.next_token = 'f'
        self.assertEqual(self.levelstate.next_id(), 'f')
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), 'f')

    def test_level_3_surf(self):
        self.levelstate.current_id = 'a-3-ii'
        self.levelstate.next_token = 'iii'
        self.assertEqual(self.levelstate.next_id(), 'a-3-iii')
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), 'iii')

    def test_level_3_dive(self):
        self.levelstate.current_id = 'd-4-iv'
        self.levelstate.next_token = 'A'
        self.assertEqual(self.levelstate.next_id(), 'd-4-iv-A')
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), 'A')

    def test_level_3_rise(self):
        self.levelstate.current_id = 'a-3-ii'
        self.levelstate.next_token = '4'
        self.assertEqual(self.levelstate.next_id(), 'a-4')
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), '4')

    def test_level_3_rise_2(self):
        self.levelstate.current_id = 'a-3-ii'
        self.levelstate.next_token = 'b'
        self.assertEqual(self.levelstate.next_id(), 'b')
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), 'b')

    def test_level_4_surf(self):
        self.levelstate.current_id = 'a-3-ii-A'
        self.levelstate.next_token = 'B'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-B')
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), 'B')

    def test_level_4_dive(self):
        self.levelstate.current_id = 'd-4-iv-A'
        self.levelstate.next_token = '1'
        self.assertEqual(self.levelstate.next_id(), 'd-4-iv-A-1')
        self.assertEqual(self.levelstate.level(), 5)
        self.assertEqual(self.levelstate.current_token(), '1')

    def test_level_4_rise(self):
        self.levelstate.current_id = 'a-3-ii-A'
        self.levelstate.next_token = 'iii'
        self.assertEqual(self.levelstate.next_id(), 'a-3-iii')
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), 'iii')

    def test_level_4_rise_2(self):
        self.levelstate.current_id = 'a-3-ii-A'
        self.levelstate.next_token = '4'
        self.assertEqual(self.levelstate.next_id(), 'a-4')
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), '4')

    def test_level_4_rise_3(self):
        self.levelstate.current_id = 'a-3-ii-A'
        self.levelstate.next_token = 'b'
        self.assertEqual(self.levelstate.next_id(), 'b')
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), 'b')

    def test_level_5_surf(self):
        self.levelstate.current_id = 'a-3-ii-A-1'
        self.levelstate.next_token = '2'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-A-2')
        self.assertEqual(self.levelstate.level(), 5)
        self.assertEqual(self.levelstate.current_token(), '2')

    def test_level_5_dive(self):
        self.levelstate.current_id = 'a-3-ii-A-2'
        self.levelstate.next_token = 'i'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-A-2-i')
        self.assertEqual(self.levelstate.level(), 6)
        self.assertEqual(self.levelstate.current_token(), 'i')

    def test_level_5_rise(self):
        self.levelstate.current_id = 'a-3-ii-A-1'
        self.levelstate.next_token = 'B'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-B')
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), 'B')

    def test_level_5_rise_2(self):
        self.levelstate.current_id = 'a-3-ii-A-1'
        self.levelstate.next_token = 'iii'
        self.assertEqual(self.levelstate.next_id(), 'a-3-iii')
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), 'iii')

    def test_level_5_rise_3(self):
        self.levelstate.current_id = 'a-3-ii-A-1'
        self.levelstate.next_token = '4'
        self.assertEqual(self.levelstate.next_id(), 'a-4')
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), '4')

    def test_level_5_rise_4(self):
        self.levelstate.current_id = 'a-3-ii-A-1'
        self.levelstate.next_token = 'b'
        self.assertEqual(self.levelstate.next_id(), 'b')
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), 'b')

    def test_level_6_surf(self):
        self.levelstate.current_id = 'a-3-ii-A-1-iv'
        self.levelstate.next_token = 'v'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-A-1-v')
        self.assertEqual(self.levelstate.level(), 6)
        self.assertEqual(self.levelstate.current_token(), 'v')

    def test_level_6_rise(self):
        self.levelstate.current_id = 'a-3-ii-A-1-iv'
        self.levelstate.next_token = '2'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-A-2')
        self.assertEqual(self.levelstate.level(), 5)
        self.assertEqual(self.levelstate.current_token(), '2')

    def test_level_6_rise_2(self):
        self.levelstate.current_id = 'a-3-ii-A-1-iv'
        self.levelstate.next_token = 'B'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-B')
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), 'B')

    def test_level_6_rise_3(self):
        self.levelstate.current_id = 'a-3-ii-A-1-iv'
        self.levelstate.next_token = 'iii'
        self.assertEqual(self.levelstate.next_id(), 'a-3-iii')
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), 'iii')

    def test_level_6_rise_4(self):
        self.levelstate.current_id = 'a-3-ii-A-1-iv'
        self.levelstate.next_token = '4'
        self.assertEqual(self.levelstate.next_id(), 'a-4')
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), '4')

    def test_level_6_rise_5(self):
        self.levelstate.current_id = 'a-3-ii-A-1-iv'
        self.levelstate.next_token = 'b'
        self.assertEqual(self.levelstate.next_id(), 'b')
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), 'b')

    def test_level_6_bad_previous_digit(self):
        self.levelstate.current_id = 'a-3-ii-A-a-iv'
        self.levelstate.next_token = 'v'
        self.assertEqual(self.levelstate.next_id(), 'a-3-ii-A-a-v')

    def test_roman_surf_test_level_3_token_not_roman(self):
        self.levelstate.current_id = 'a-1-1'
        self.assertIs(self.levelstate.roman_surf_test(), False)

    def test_roman_surf_test_true(self):
        self.levelstate.current_id = 'a-1-i'
        self.levelstate.next_token = 'ii'
        self.assertIs(self.levelstate.roman_surf_test(), True)


class EtruscanTestCase(unittest.TestCase):
    """Testing the Roman functions"""

    tokens = {
        'i': 1,
        'ii': 2,
        'iii': 3,
        'iv': 4,
        'v': 5,
        'vi': 6,
        'vii': 7,
        'viii': 8,
        'ix': 9,
        'x': 10,
        'xi': 11,
        'xl': 40,
        'l': 50,
        'c': 100
    }

    def test_roman_to_int(self):
        for token in self.tokens:
            self.assertEqual(roman_to_int(token), self.tokens[token])

    def test_int_to_roman(self):
        for key, value in self.tokens.items():
            self.assertEqual(int_to_roman(value), key)

    def test_int_to_roman_invalid_type(self):
        self.assertIs(roman_to_int(1), None)

    def test_int_to_roman_invalid_sequence(self):
        self.assertIs(roman_to_int('ic'), None)

    def test_int_to_roman_non_integer(self):
        with self.assertRaises(TypeError):
            int_to_roman('A')

    def test_int_to_roman_out_of_range(self):
        with self.assertRaises(ValueError):
            int_to_roman(4000)
