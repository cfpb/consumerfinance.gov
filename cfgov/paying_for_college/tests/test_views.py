from __future__ import unicode_literals

import copy
import json
import unittest

import django
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import RequestFactory

import mock
from paying_for_college.models import Program, School
from paying_for_college.views import (
    EXPENSE_FILE, Feedback, get_json_file, get_program, get_program_length,
    get_school, school_search_api, validate_oid, validate_pid
)


# def setup_view(view, request, *args, **kwargs):
#     """Mimic as_view() returned callable, return view instance instead."""
#     view.request = request
#     view.args = args
#     view.kwargs = kwargs
#     return view


class Validators(unittest.TestCase):
    """check the oid validator"""
    max_oid = (
        '6ca1a60a72b3d4640b20a683d63a40297b7c45c4df479cd93cd57d9c44820069'
        'eb71d168eedd531bb488cd2e58d3dbbce8ee80c02ef6fc9623479510adedf704')
    good_oid = '9e0280139f3238cbc9702c7b0d62e5c238a835d0'
    bad_oid = '9e0<script>console.log("hi")</script>5d0'
    short_oid = '9e45a3e7'

    def test_validate_oid(self):
        self.assertFalse(validate_oid(self.bad_oid))
        self.assertFalse(validate_oid(self.short_oid))
        self.assertTrue(validate_oid(self.good_oid))
        self.assertTrue(validate_oid(self.max_oid))

    def test_validate_pid(self):
        # bad_chars = [';', '<', '>', '{', '}']
        self.assertFalse(validate_pid('490<script>'))
        self.assertFalse(validate_pid('{value}'))
        self.assertFalse(validate_pid('DROP TABLE;'))
        self.assertTrue(validate_pid('108b'))


class TestViews(django.test.TestCase):

    landing_page_views = [
        'pfc-landing',
        'pfc-repay',
        'pfc-choose',
        'pfc-manage',
    ]
    POST = HttpRequest()
    POST.POST = {'school_program': '999999',
                 'ba': True,
                 'is_valid': True}
    feedback_post_data = {'csrfmiddlewaretoken': 'abc',
                          'message': 'test',
                          'referrer': 'disclosure/page'}

    def test_get_json_file(self):
        test_json = get_json_file(EXPENSE_FILE)
        test_data = json.loads(test_json)
        self.assertTrue('Other' in test_data.keys())
        test_json2 = get_json_file('xxx')
        self.assertTrue(test_json2 == '')

    def test_get_program_length(self):
        school = School(school_id=123456, degrees_highest='2')
        program = Program(institution=school, level='2')
        bad_school = School(school_id=999999, degrees_highest='5')
        test1 = get_program_length(program=program, school=school)
        self.assertTrue(test1 == 2)
        test2 = get_program_length(program='', school=school)
        self.assertTrue(test2 == 2)
        test3 = get_program_length(program='', school='')
        self.assertIs(test3, None)
        program.level = '3'
        test4 = get_program_length(program=program, school='')
        self.assertEqual(test4, 4)
        bad_school_test = get_program_length(program='', school=bad_school)
        self.assertIs(bad_school_test, None)

    def test_feedback(self):
        response = self.client.get(reverse(
            'paying_for_college:disclosures:pfc-feedback'))
        self.assertEqual(
            sorted(list(response.context_data.keys())),
            ['form', 'url_root']
        )

    def test_feedback_post_creates_feedback(self):
        self.assertFalse(Feedback.objects.exists())
        self.client.post(
            reverse('paying_for_college:disclosures:pfc-feedback'),
            data=self.feedback_post_data)
        self.assertTrue(Feedback.objects.exists())

    def test_feedback_post_invalid(self):
        response = self.client.post(reverse(
            'paying_for_college:disclosures:pfc-feedback'))
        self.assertTrue(response.status_code == 400)

    def test_technote(self):
        response = self.client.get(reverse(
            'paying_for_college:disclosures:pfc-technote'))
        self.assertTrue('url_root' in response.context_data.keys())


# understanding-financial-aid-offers/api/search-schools.json?q=Kansas
class SchoolSearchTest(django.test.TestCase):

    fixtures = ['test_fixture.json',
                'test_program.json']

    class ElasticSchool:
        def __init__(self):
            self.text = ''
            self.school_id = 0
            self.city = ''
            self.state = ''
            self.nicknames = ''

    def test_get_school(self):
        """test grabbing a school by ID"""
        closed_school = School(pk=999999, operating=False)
        closed_school.save()
        test1 = get_school('155317')
        self.assertTrue(test1.pk == 155317)
        test2 = get_school('xxx')
        self.assertTrue(test2 is None)
        test3 = get_school('999999')
        self.assertTrue(test3 is None)

    def test_get_program(self):
        """test grabbing a program by school/program_code"""
        school = School.objects.get(school_id=408039)
        test1 = get_program(school, '981')
        self.assertTrue('Occupational' in test1.program_name)
        test2 = get_program(school, 'xxx')
        self.assertIs(test2, None)
        test3 = get_program(school, '<program>')
        self.assertIs(test3, None)

    @mock.patch('paying_for_college.views.SearchQuerySet.autocomplete')
    def test_school_search_api(self, mock_sqs_autocomplete):
        """school_search_api should return json."""

        mock_school = School.objects.get(pk=155317)
        # mock the search returned value
        elastic_school = self.ElasticSchool()
        elastic_school.text = mock_school.primary_alias
        elastic_school.school_id = mock_school.school_id
        elastic_school.city = mock_school.city
        elastic_school.state = mock_school.state
        elastic_school.nicknames = 'Jayhawks'
        solr_queryset = [elastic_school]
        mock_sqs_autocomplete.return_value = solr_queryset
        url = "{}?q=Kansas".format(reverse(
            'paying_for_college:disclosures:school_search'
        ))
        request = RequestFactory().get(url)
        resp = school_search_api(request)
        self.assertTrue(b'Kansas' in resp.content)
        self.assertTrue(b'155317' in resp.content)
        self.assertTrue(b'Jayhawks' in resp.content)


class OfferTest(django.test.TestCase):

    fixtures = ['test_fixture.json',
                'test_program.json']

    # /paying-for-college/understanding-financial-aid-offers/offer/?[QUERYSTRING]
    def test_offer(self):
        """request for offer disclosure."""

        url = reverse('paying_for_college:disclosures:offer')
        # offer_test_url = reverse('paying_for_college:disclosures:offer_test')
        qstring = ('?iped=408039&pid=981&'
                   'oid=f38283b5b7c939a058889f997949efa566c616c5&'
                   'tuit=38976&hous=3000&book=650&tran=500&othr=500&'
                   'pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&'
                   'mta=3000&gib=3000&wkst=3000&parl=10000&perl=3000&'
                   'subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&'
                   'prvi=4.55&insl=3000&insi=4.55')
        no_oid = '?iped=408039&pid=981&oid='
        bad_school = ('?iped=xxxxxx&pid=981&'
                      'oid=f38283b5b7c939a058889f997949efa566c61')
        bad_program = ('?iped=408039&pid=xxx&'
                       'oid=f38283b5b7c939a058889f997949efa566c616c5')
        # puerto_rico = '?iped=243197&pid=981&oid='
        missing_oid_field = '?iped=408039&pid=981'
        missing_school_id = '?iped='
        bad_oid = ('?iped=408039&pid=981&oid=f382'
                   '<script></script>f997949efa566c616c5')
        illegal_program = ('?iped=408039&pid=<981>&oid=f38283b'
                           '5b7c939a058889f997949efa566c616c5')
        no_program = ('?iped=408039&pid=&oid=f38283b'
                      '5b7c939a058889f997949efa566c616c5')
        resp = self.client.get(url + qstring)
        self.assertTrue(resp.status_code == 200)
        resp_test = self.client.get(url + qstring)
        self.assertTrue(resp_test.status_code == 200)
        resp2 = self.client.get(url + no_oid)
        self.assertTrue(resp2.status_code == 200)
        self.assertTrue("noOffer" in resp2.context['warning'])
        resp3 = self.client.get(url + bad_school)
        self.assertTrue("noSchool" in resp3.context['warning'])
        self.assertTrue(resp3.status_code == 200)
        resp4 = self.client.get(url + bad_program)
        self.assertTrue(resp4.status_code == 200)
        self.assertTrue("noProgram" in resp4.context['warning'])
        resp5 = self.client.get(url + missing_oid_field)
        self.assertTrue(resp5.status_code == 200)
        self.assertTrue("noOffer" in resp5.context['warning'])
        resp6 = self.client.get(url + missing_school_id)
        self.assertTrue("noSchool" in resp6.context['warning'])
        self.assertTrue(resp6.status_code == 200)
        resp7 = self.client.get(url + bad_oid)
        self.assertTrue("noOffer" in resp7.context['warning'])
        self.assertTrue(resp7.status_code == 200)
        resp8 = self.client.get(url + illegal_program)
        self.assertTrue("noProgram" in resp8.context['warning'])
        self.assertTrue(resp8.status_code == 200)
        resp9 = self.client.get(url + no_program)
        self.assertTrue("noProgram" in resp9.context['warning'])
        self.assertTrue(resp9.status_code == 200)
        resp10 = self.client.get(url)
        self.assertTrue(resp10.context['warning'] == '')
        self.assertTrue(resp10.status_code == 200)


class APITests(django.test.TestCase):

    fixtures = ['test_fixture.json',
                'test_constants.json',
                'test_program.json']

    # /paying-for-college/understanding-financial-aid-offers/api/school/155317.json
    def test_school_json(self):
        """api call for school details."""

        url = reverse(
            'paying_for_college:disclosures:school-json', args=['155317'])
        resp = self.client.get(url)
        self.assertIn(b'Kansas', resp.content)
        self.assertIn(b'155317', resp.content)

    # /paying-for-college/understanding-financial-aid-offers/api/constants/
    def test_constants_json(self):
        """api call for constants."""

        url = reverse('paying_for_college:disclosures:constants-json')
        resp = self.client.get(url)
        self.assertIn(b'institutionalLoanRate', resp.content)
        self.assertIn(b'apiYear', resp.content)

    # /paying-for-college/understanding-financial-aid-offers/api/constants/
    def test_national_stats_json(self):
        """api call for national statistics."""

        url = reverse(
            'paying_for_college:disclosures:national-stats-json',
            args=['408039'])
        resp = self.client.get(url)
        self.assertIn(b'retentionRateMedian', resp.content)
        self.assertEqual(resp.status_code, 200)
        url2 = reverse(
            'paying_for_college:disclosures:national-stats-json',
            args=['000000'])
        resp2 = self.client.get(url2)
        self.assertIn(b'nationalSalary', resp2.content)
        self.assertEqual(resp2.status_code, 200)

    def test_expense_json(self):
        """api call for BLS expense data"""
        url = reverse('paying_for_college:disclosures:expenses-json')
        resp = self.client.get(url)
        self.assertIn(b'Other', resp.content)

    @mock.patch('paying_for_college.views.get_json_file')
    def test_expense_json_failure(self, mock_get_json):
        """failed api call for BLS expense data"""
        url = reverse('paying_for_college:disclosures:expenses-json')
        mock_get_json.return_value = ''
        resp = self.client.get(url)
        self.assertIn(b'No expense', resp.content)

    # /paying-for-college/understanding-financial-aid-offers/api/program/408039_981/
    def test_program_json(self):
        """api call for program details."""

        url = reverse(
            'paying_for_college:disclosures:program-json', args=['408039_981'])
        resp = self.client.get(url)
        self.assertIn(b'housing', resp.content)
        self.assertIn(b'books', resp.content)
        bad_url = reverse(
            'paying_for_college:disclosures:program-json', args=['408039'])
        resp2 = self.client.get(bad_url)
        self.assertEqual(resp2.status_code, 400)
        self.assertTrue(b'Error' in resp2.content)
        url3 = reverse(
            'paying_for_college:disclosures:program-json', args=['408039_xyz'])
        resp3 = self.client.get(url3)
        self.assertEqual(resp3.status_code, 400)
        self.assertIn(b'Error', resp3.content)
        url4 = reverse(
            'paying_for_college:disclosures:program-json',
            args=['408039_<script>'])
        resp4 = self.client.get(url4)
        self.assertEqual(resp4.status_code, 400)
        self.assertIn(b'Error', resp4.content)
        url5 = reverse(
            'paying_for_college:disclosures:program-json', args=['x08039_981'])
        resp5 = self.client.get(url5)
        self.assertEqual(resp5.status_code, 400)
        self.assertIn(b'Error', resp5.content)


class VerifyViewTest(django.test.TestCase):

    fixtures = ['test_fixture.json']
    post_data = {'oid': 'f38283b5b7c939a058889f997949efa566c616c5',
                 'iped': '243197',
                 'errors': 'none',
                 'URL': 'fake-url.com'}
    url = reverse('paying_for_college:disclosures:verify')

    def test_verify_view(self):
        resp = self.client.post(self.url, data=self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Verification', resp.content)
        resp2 = self.client.post(self.url, data=self.post_data)
        self.assertEqual(resp2.status_code, 400)
        self.assertIn(b'already', resp2.content)

    def test_verify_view_school_has_no_contact(self):
        post_data = copy.copy(self.post_data)
        post_data['iped'] = '408039'
        post_data['oid'] = 'f38283b5b7c939a058889f997949efa566c616c4'
        resp = self.client.post(self.url, data=post_data)
        self.assertEqual(resp.status_code, 400)

    def test_verify_view_bad_id(self):
        self.post_data['iped'] = ''
        resp = self.client.post(self.url, data=self.post_data)
        self.assertEqual(resp.status_code, 400)

    def test_verify_view_bad_oid(self):
        self.post_data['iped'] = '243197'
        self.post_data['oid'] = 'f38283b5b7c939a058889f997949efa566script'
        resp = self.client.post(self.url, data=self.post_data)
        self.assertEqual(resp.status_code, 400)

    def test_verify_view_no_data(self):
        self.post_data = {}
        resp = self.client.post(self.url, data=self.post_data)
        self.assertEqual(resp.status_code, 400)
