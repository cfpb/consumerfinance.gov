# -*- coding: utf-8 -*-
from unittest import mock
from unittest.mock import mock_open, patch

import django

from paying_for_college.disclosures.scripts.load_programs import (
    clean, clean_number_as_string, clean_string_as_string, get_school, load,
    read_in_data, read_in_s3, standardize_rate
)
from paying_for_college.models import Program, School


class TestLoadPrograms(django.test.TestCase):
    fixtures = ['test_program.json']
    read_out = [{
        'accreditor': '',
        'average_time_to_complete': '',
        'books_supplies': '0',
        'campus_name': 'Argosy University, San Francisco Bay Area',
        'cip_code': '11.0103',
        'completers': '',
        'completion_cohort': '',
        'completion_rate': 'None',
        'default_rate': 'None',
        'ipeds_unit_id': '121983',
        'job_placement_note': '',
        'job_placement_rate': 'None',
        'mean_student_loan_completers': '',
        'median_salary': '',
        'median_student_loan_completers': '17681',
        'ope_id': '',
        'program_code': 'TEST1',
        'program_length': '20',
        'program_level': '2',
        'program_name': 'Information Technology',
        'soc_codes': '',
        'test': 'True',
        'total_cost': '33859',
        'tuition_fees': '33859',
    }]
    to_cleanup = {
        'job_placement_rate': '80',
        'default_rate': '0.29',
        'job_placement_note': '',
        'mean_student_loan_completers': 'Blank',
        'average_time_to_complete': '',
        'accreditor': '',
        'total_cost': '44565',
        'ipeds_unit_id': '139579',
        'median_salary': '45586',
        'program_code': '1509',
        'books_supplies': 'No Data',
        'campus_name': 'SU Savannah',
        'cip_code': '11.0401',
        'ope_id': '1303900',
        'completion_rate': '0.23',
        'program_level': '2',
        'tuition_fees': '44565',
        'program_name': 'Information Technology',
        'median_student_loan_completers': '28852',
        'program_length': '24',
        'completers': '0',
        'completion_cohort': '0',
    }
    cleaned = {
        'job_placement_rate': 'NUMBER',
        'default_rate': 'NUMBER',
        'job_placement_note': 'STRING',
        'mean_student_loan_completers': 'NUMBER',
        'average_time_to_complete': 'NUMBER',
        'accreditor': 'STRING',
        'total_cost': 'NUMBER',
        'ipeds_unit_id': 'STRING',
        'median_salary': 'NUMBER',
        'program_code': 'STRING',
        'books_supplies': 'NUMBER',
        'campus_name': 'STRING',
        'cip_code': 'STRING',
        'ope_id': 'STRING',
        'completion_rate': 'NUMBER',
        'program_level': 'NUMBER',
        'tuition_fees': 'NUMBER',
        'program_name': 'STRING',
        'median_student_loan_completers': 'NUMBER',
        'program_length': 'NUMBER',
        'completers': 'NUMBER',
        'completion_cohort': 'NUMBER',
    }

    def setUp(self):
        print_patch = mock.patch(
            'paying_for_college.disclosures.scripts.load_programs.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

    def test_standardize_rate(self):
        self.assertTrue(standardize_rate('1.7') == '0.017')
        self.assertTrue(standardize_rate('0.017') == '0.017')

    def test_get_school_valid(self):
        result_school, result_err = get_school("408039")
        self.assertEqual(result_school, School.objects.first())
        self.assertEqual(result_err, '')

    def test_get_school_invalid(self):
        result_school, result_err = get_school("1")
        self.assertEqual(result_school, '')
        self.assertEqual(result_err, "ERROR: couldn't find school for ID 1")

    def test_clean_number_as_string_normal_string(self):
        result = clean_number_as_string(" Test Data  ")
        self.assertEqual(result, "Test Data")

    def test_clean_number_as_string_empty_string(self):
        result = clean_number_as_string("  ")
        self.assertEqual(result, None)

    def test_clean_number_as_string_blank(self):
        result = clean_number_as_string("  Blank  ")
        self.assertEqual(result, None)

    def test_clean_number_as_string_no_grad(self):
        result = clean_number_as_string("  No Grads ")
        self.assertEqual(result, None)

    def test_clean_number_as_string_no_data(self):
        result = clean_number_as_string("  No Data ")
        self.assertEqual(result, None)

    def test_clean_string_as_string_normal(self):
        result = clean_string_as_string(" Normal Data  ")
        self.assertEqual(result, "Normal Data")

    def test_clean_string_as_string_empty_string(self):
        result = clean_string_as_string("  ")
        self.assertEqual(result, '')

    def test_clean_string_as_string_blank(self):
        result = clean_string_as_string("  Blank  ")
        self.assertEqual(result, '')

    def test_clean_string_as_string_no_grad(self):
        result = clean_string_as_string("  No Grads ")
        self.assertEqual(result, '')

    def test_clean_string_as_string_no_data(self):
        result = clean_string_as_string("  No Data ")
        self.assertEqual(result, '')

    def test_read_in_data(self):
        # mock_return = [{'a': 'd', 'b': 'e', 'c': 'f'}]
        m = mock_open(read_data='a,b,c\nd,e,f')
        with patch("builtins.open", m):
            read_in_data('mockfile.csv')
        self.assertEqual(m.call_count, 1)
        # self.assertEqual(data, mock_return)
        # m2 = mock_open(read_data='a,b,c\nd,e,f')
        # m2.side_effect = UnicodeDecodeError
        # with patch("builtins.open", m2):
        #     read_in_data('mockfile.csv')
        # self.assertEqual(m.call_count, 2)
        # self.assertEqual(data, mock_return)

    @patch(
        'paying_for_college.disclosures.scripts.load_programs.requests.get')
    def test_read_in_s3(self, mock_requests):
        mock_requests.return_value.text = (
            'a,b,c\nd,e,\u201c')
        data = read_in_s3('fake-s3-url.com')
        self.assertEqual(
            mock_requests.call_count,
            1
        )
        self.assertEqual(
            data,
            [{'a': 'd', 'b': 'e', 'c': '\u201c'}]
        )

    @patch(
        'paying_for_college.disclosures.scripts'
        '.load_programs.clean_number_as_string')
    @patch(
        'paying_for_college.disclosures.scripts.'
        'load_programs.clean_string_as_string')
    @patch(
        'paying_for_college.disclosures.scripts.'
        'load_programs.standardize_rate')
    def test_clean(self, mock_standardize, mock_string, mock_number):
        mock_number.return_value = 'NUMBER'
        mock_string.return_value = 'STRING'
        mock_standardize.return_value = 'NUMBER'
        result = clean(self.to_cleanup)
        self.assertEqual(mock_number.call_count, 14)
        self.assertEqual(mock_string.call_count, 8)
        self.assertDictEqual(result, self.cleaned)

    @patch(
        'paying_for_college.disclosures.scripts.load_programs.read_in_s3')
    def test_load_s3(self, mock_read_in_s3):
        mock_read_in_s3.return_value = self.read_out
        (FAILED, msg) = load('mockurl', s3=True)
        self.assertTrue(mock_read_in_s3.call_count == 1)
        self.assertEqual(FAILED, [])
        self.assertIn('0 programs created', msg)

    @patch(
        'paying_for_college.disclosures.scripts.load_programs.read_in_s3')
    def test_load_s3_failure(self, mock_read_in_s3):
        mock_read_in_s3.return_value = [{}]
        (FAILED, msg) = load('mockurl', s3=True)
        self.assertTrue(mock_read_in_s3.call_count == 1)
        self.assertTrue('ERROR' in FAILED[0])

    @patch(
        'paying_for_college.disclosures.scripts.load_programs.read_in_data')
    @patch(
        'paying_for_college.disclosures.scripts.load_programs.clean')
    @patch(
        'paying_for_college.disclosures.scripts.'
        'load_programs.Program.objects.get_or_create')
    def test_load(self, mock_get_or_create_program, mock_clean, mock_read_in):
        accreditor = (
            "Accrediting Council for Independent Colleges "
            "and Schools (ACICS) - Test")
        jpr_note = (
            "The rate reflects employment status "
            "as of November 1, 2014 - Test")
        program_name = "Occupational Therapy Assistant - 981 - Test"
        mock_read_in.return_value = [
            {"ipeds_unit_id": "408039",
             "ope_id": "",
             "campus_name": "Ft Wayne - Test",
             "program_code": "981 - Test",
             "program_name": program_name,
             "program_level": "4",
             "program_length": "25",
             "accreditor": accreditor,
             "median_salary": "24000",
             "average_time_to_complete": "35",
             "books_supplies": "1000",
             "completion_rate": "13",
             "default_rate": "50",
             "job_placement_rate": "0.20",
             "job_placement_note": jpr_note,
             "mean_student_loan_completers": "30000",
             "median_student_loan_completers": "30500",
             "total_cost": "50000",
             "tuition_fees": "40000",
             "cip_code": "51.0803 - Test",
             "completers": "0",
             "completion_cohort": "0"}
        ]
        mock_clean.return_value = {
            "ipeds_unit_id": "408039",
            "ope_id": "",
            "campus_name": "Ft Wayne - Test",
            "program_code": "981 - Test",
            "program_name": program_name,
            "program_level": 4,
            "program_length": 25,
            "accreditor": accreditor,
            "median_salary": 24000,
            "average_time_to_complete": 35,
            "books_supplies": 1000,
            "completion_rate": 13,
            "default_rate": 50,
            "job_placement_rate": 0.20,
            "job_placement_note": jpr_note,
            "mean_student_loan_completers": 30000,
            "median_student_loan_completers": 30500,
            "total_cost": 50000,
            "tuition_fees": 40000,
            "cip_code": "51.0803 - Test",
            "completers": 0,
            "completion_cohort": 0}
        program = Program.objects.first()
        mock_get_or_create_program.return_value = (program, False)

        load("filename")
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(mock_clean.call_count, 1)
        self.assertEqual(mock_get_or_create_program.call_count, 1)
        self.assertEqual(program.accreditor, accreditor)
        self.assertEqual(program.cip_code, "51.0803 - Test")
        self.assertEqual(program.completion_rate, 13.00)
        self.assertEqual(program.default_rate, 50.00)
        self.assertEqual(program.mean_student_loan_completers, 30000)
        self.assertEqual(program.median_student_loan_completers, 30500)
        self.assertEqual(program.program_code, "981 - Test")
        self.assertEqual(
            program.program_name,
            "Occupational Therapy Assistant - 981 - Test"
        )
        self.assertEqual(program.program_length, 25)
        self.assertEqual(program.total_cost, 50000)
        self.assertEqual(program.campus, "Ft Wayne - Test")
        self.assertEqual(program.level, 4)
        self.assertEqual(program.time_to_complete, 35)
        self.assertEqual(program.salary, 24000)
        self.assertEqual(program.job_rate, 0.20)
        self.assertEqual(program.job_note, jpr_note)
        self.assertEqual(program.tuition, 40000)
        self.assertEqual(program.books, 1000)
        self.assertEqual(program.completers, 0)
        self.assertEqual(program.completion_cohort, 0)
        mock_clean.return_value['ipeds_unit_id'] = '9'
        load('filename')
        self.assertEqual(mock_read_in.call_count, 2)
        self.assertEqual(mock_get_or_create_program.call_count, 1)
        mock_clean.return_value['program_code'] = '<904>'
        load('filename')
        self.assertEqual(mock_read_in.call_count, 3)
        self.assertEqual(
            mock_get_or_create_program.call_count,
            1)  # loader bails before creating program
        mock_clean.return_value['ipeds_unit_id'] = "408039"
        mock_clean.return_value['program_code'] = "99982"
        mock_get_or_create_program.return_value = (program, True)
        load('filename')
        self.assertEqual(mock_read_in.call_count, 4)
        mock_read_in.return_value[0]['test'] = "True"
        load('filename')
        self.assertEqual(mock_read_in.call_count, 5)

    @patch(
        'paying_for_college.disclosures.scripts.load_programs.clean')
    @patch(
        'paying_for_college.disclosures.scripts.load_programs.read_in_data')
    def test_load_error(self, mock_read_in, mock_clean):
        mock_read_in.return_value = [{}]
        (FAILED, endmsg) = load("filename")
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(mock_clean.call_count, 0)  # bailed before cleaning
        self.assertTrue('ERROR' in " ".join(FAILED))
        mock_read_in.return_value = [{'raw_data': 'raw stuff'}]
        mock_clean.return_value = {'cleaned_data': 'clean stuff'}
        (FAILED, endmsg) = load("filename")
        self.assertEqual(mock_read_in.call_count, 2)
        self.assertEqual(mock_clean.call_count, 1)
        self.assertTrue('ERROR' in " ".join(FAILED))
