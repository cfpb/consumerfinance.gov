# -*- coding: utf-8 -*-
import io
from csv import DictReader as cdr

import requests
from rest_framework import serializers

from paying_for_college.models import Program, School
from paying_for_college.views import validate_pid


NO_DATA_ENTRIES_LOWER = ('', 'blank', 'no grads', 'no data', 'none')

"""
# Program Data Processing Steps

This script was used to process program data from schools.

It takes in a csv file with column labels as described in ProgramSerializer.

To run the script, use this manage.py command:

```
./manage.py load_programs [PATH TO CSV or s3 filename]
```
"""


class ProgramSerializer(serializers.Serializer):

    # required fields
    ipeds_unit_id = serializers.CharField(max_length=6)  # '210960'
    program_code = serializers.CharField(max_length=255)
    program_name = serializers.CharField(max_length=255)
    program_level = serializers.IntegerField(min_value=0, max_value=4)
    program_length = serializers.IntegerField(max_value=120)  # in months
    total_cost = serializers.IntegerField()
    tuition_fees = serializers.IntegerField()
    books_supplies = serializers.IntegerField()
    # allowed to be missing or blank
    ope_id = serializers.CharField(  # '02117100'
        max_length=8,
        allow_blank=True,
        required=False)
    campus_name = serializers.CharField(
        max_length=255,
        allow_blank=True,
        required=False)
    accreditor = serializers.CharField(
        allow_blank=True,
        required=False)
    median_salary = serializers.IntegerField(  # 31240
        allow_null=True,
        required=False)
    average_time_to_complete = serializers.IntegerField(  # 36
        allow_null=True,
        required=False)
    completion_rate = serializers.FloatField(  # 0.29
        allow_null=True,
        required=False)
    default_rate = serializers.FloatField(  # 0.23
        allow_null=True,
        required=False)
    job_placement_rate = serializers.FloatField(  # 0.7
        allow_null=True,
        required=False)
    job_placement_note = serializers.CharField(
        allow_blank=True,
        required=False)
    mean_student_loan_completers = serializers.IntegerField(
        allow_null=True,
        required=False)
    median_student_loan_completers = serializers.IntegerField(
        allow_null=True,
        required=False)
    cip_code = serializers.CharField(  # '12.0504'
        allow_blank=True,
        required=False)
    completers = serializers.IntegerField(
        allow_null=True,
        required=False)
    completion_cohort = serializers.IntegerField(
        allow_null=True,
        required=False)
    # OUR DATABASE HAS A SOC_CODES FIELD but we're not using it for now
    # soc_codes = serializers.CharField(  # '35-1011, 35-1012'
    #     allow_blank=True,
    #     required=False)


def get_school(iped):
    try:
        school = School.objects.get(school_id=int(iped))
    except Exception:
        return ('', "ERROR: couldn't find school for ID {0}".format(iped))
    else:
        return (school, '')


def read_in_data(filename):
    """Read in a utf-8 CSV, as per our spec, or windows-1252 if we must."""
    try:
        with open(filename, newline='', encoding='utf-8-sig') as f:
            reader = cdr(f)
            data = [row for row in reader]
    except UnicodeDecodeError:
        try:
            with open(filename, newline='', encoding='windows-1252') as f:
                reader = cdr(f)
                data = [row for row in reader]
        except Exception:
            data = [{}]
    except Exception:
        data = [{}]
    return data


def read_in_s3(url):
    response = requests.get(url)
    f = io.StringIO(response.text)
    reader = cdr(f)
    data = [row for row in reader]
    return data


def clean_number_as_string(string):
    # This needs to be cleaned up to None, else validation will complain
    clean_str = string.strip()
    return (
        clean_str if clean_str.lower() not in NO_DATA_ENTRIES_LOWER else None
    )


def clean_string_as_string(string):
    clean_str = string.strip()
    return clean_str if clean_str.lower() not in NO_DATA_ENTRIES_LOWER else ''


def standardize_rate(rate):
    if rate and float(rate) > 1:
        return str(float(rate) / 100)
    else:
        return rate


def strip_control_chars(ustring):
    return ustring.replace(u'\x97', u'-').replace(u'\x96', u'-')


def clean(data):

    number_fields = (
        'program_level', 'program_length', 'median_salary',
        'average_time_to_complete', 'books_supplies', 'completion_rate',
        'default_rate', 'job_placement_rate', 'mean_student_loan_completers',
        'median_student_loan_completers', 'total_cost', 'tuition_fees',
        'completers', 'completion_cohort'
    )
    rate_fields = ('completion_rate', 'default_rate', 'job_placement_rate')
    # Clean string and numeric parameters
    cleaned_data = {
        k: clean_number_as_string(v) for k, v in dict.items(data)
        if k in number_fields
    }
    cleaned_data.update(
        {
            k: clean_string_as_string(v) for k, v in dict.items(data)
            if k not in number_fields
        }
    )
    for rate in rate_fields:
        cleaned_data[rate] = standardize_rate(cleaned_data[rate])
    cleaned_data['ope_id'] = cleaned_data['ope_id'].replace(
        '-', '').replace(
        ' ', '')

    return cleaned_data


def load(source, s3=False):
    """
    Loads program data from a local or S3 file.
    For a local file, 'source' should be a CSV file path.
    For an s3 file, 'source' should be the file name of a CSV
    in the 'validated_program_data' folder on s3.
    """
    test_program = False
    new_programs = 0
    updated_programs = 0
    FAILED = []  # failed messages
    if s3:
        s3_url = ('https://files.consumerfinance.gov'
                  '/pb/paying_for_college/csv/validated_program_data/{}')
        raw_data = read_in_s3(s3_url.format(source))
    else:
        raw_data = read_in_data(source)
    if not raw_data[0]:
        return (["ERROR: could not read data from {0}".format(source)], "")

    for row in raw_data:
        if 'test' in row.keys() and row['test'].lower() == 'true':
            test_program = True
        fixed_data = clean(row)
        serializer = ProgramSerializer(data=fixed_data)

        if serializer.is_valid():
            data = serializer.validated_data
            if not validate_pid(data['program_code']):
                print("ERROR: invalid program code: "
                      "{}".format(data['program_code']))
                continue
            (school, error) = get_school(data['ipeds_unit_id'])
            if error:
                print(error)
                continue

            program, cr = Program.objects.get_or_create(
                institution=school,
                program_code=data['program_code']
            )
            if cr:
                new_programs += 1
            else:
                updated_programs += 1

            program.accreditor = data['accreditor']
            program.cip_code = data['cip_code']
            program.completion_rate = data['completion_rate']
            program.default_rate = data['default_rate']
            program.mean_student_loan_completers = data['mean_student_'
                                                        'loan_completers']
            program.median_student_loan_completers = data['median_student_'
                                                          'loan_completers']
            program.program_code = data['program_code']
            program.program_name = strip_control_chars(data['program_name'])
            program.program_length = data['program_length']
            # program.soc_codes = data['soc_codes']
            program.total_cost = data['total_cost']

            program.campus = strip_control_chars(data['campus_name'])
            program.level = data['program_level']
            program.time_to_complete = data['average_time_to_complete']
            program.salary = data['median_salary']
            program.job_rate = data['job_placement_rate']
            program.job_note = data['job_placement_note']
            program.tuition = data['tuition_fees']
            program.books = data['books_supplies']
            program.completers = data['completers']
            program.completion_cohort = data['completion_cohort']
            program.test = test_program
            program.save()

        else:  # There is error
            for key, error_list in dict.items(serializer.errors):

                fail_msg = (
                    'ERROR on row {}: {}: '.format(
                        raw_data.index(row) + 1, key))
                for e in error_list:
                    fail_msg = '{} {},'.format(fail_msg, e)
                FAILED.append(fail_msg)

    endmsg = ('{} programs created. '
              '{} programs updated.'.format(new_programs, updated_programs))

    return (FAILED, endmsg)
