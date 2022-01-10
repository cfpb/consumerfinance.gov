import datetime

from django.test import RequestFactory, TestCase

from model_bakery import baker

from regulations3k.models import EffectiveVersion, Part
from regulations3k.views import get_version_date, redirect_eregs


class RedirectRegulations3kTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.test_reg_1002 = baker.make(
            Part,
            part_number='1002')

        self.test_reg_1005 = baker.make(
            Part,
            part_number='1005')

        self.test_version_1002 = baker.make(
            EffectiveVersion,
            part=self.test_reg_1002,
            effective_date=datetime.date(2016, 7, 11),
            draft=False)

        self.test_version_1002_2011 = baker.make(
            EffectiveVersion,
            part=self.test_reg_1002,
            effective_date=datetime.date(2011, 12, 30),
            draft=False)

        self.test_version_1002_not_live = baker.make(
            EffectiveVersion,
            part=self.test_reg_1002,
            effective_date=datetime.date(2014, 1, 10),
            draft=True)

        self.test_version_1005 = baker.make(
            EffectiveVersion,
            part=self.test_reg_1005,
            effective_date=datetime.date(2013, 3, 26),
            draft=False)

    def test_redirect_base_url(self):
        request = self.factory.get('/eregulations/')
        response = redirect_eregs(request)
        self.assertEqual(response.get('location'),
                         '/policy-compliance/rulemaking/regulations/')

    def test_redirect_reg_base_url(self):
        request = self.factory.get('/eregulations/1002')
        response = redirect_eregs(request)
        self.assertEqual(response.get('location'),
                         '/policy-compliance/rulemaking/regulations/1002/')

    def test_redirect_reg_section_url(self):
        request = self.factory.get(
            '/eregulations/1002-1/2017-20417_20180101')
        response = redirect_eregs(request)
        self.assertEqual(response.get('location'),
                         '/policy-compliance/rulemaking/regulations/1002/1/')

    def test_redirect_search(self):
        request = self.factory.get(
            '/eregulations/search/1002',
            {'q': 'california', 'version': '2011-1'})
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/'
            'search-regulations/results/?regs=1002&q=california')

    def test_redirect_search_invalid(self):
        request = self.factory.get(
            '/eregulations/search/1002',
        )
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/'
            'search-regulations/results/?regs=1002&q=')

    def test_redirect_invalid_part(self):
        request = self.factory.get(
            '/eregulations/1020-1/2017-20417_20180101')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/')

    def test_redirect_invalid_part_pattern(self):
        request = self.factory.get(
            '/eregulations/102/')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/')

    def test_redirect_past_version(self):
        request = self.factory.get(
            '/eregulations/1002-1/2016-16301')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/2016-07-11/1/')

    def test_redirect_past_version_not_live(self):
        request = self.factory.get(
            '/eregulations/1002-1/2013-22752_20140110')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/1/')

    def test_redirect_interp_appendix(self):
        request = self.factory.get(
            '/eregulations/1002-Appendices-Interp/2016-16301')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/'
            '1002/2016-07-11/interp-c/')

    def test_redirect_interp_appendix_invalid_date(self):
        request = self.factory.get(
            '/eregulations/1024-Appendices-Interp/2017-20417_20180101')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1024/interp-ms/')

    def test_redirect_interp_intro(self):
        request = self.factory.get(
            '/eregulations/1002-Interp-h1/2016-16301')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/'
            '2016-07-11/h1-interp/')

    def test_redirect_interp_intro_bad_version(self):
        request = self.factory.get(
            '/eregulations/1030-Interp-h1/2011-31727')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1030/interp-0/')

    def test_redirect_interp_section_past(self):
        request = self.factory.get(
            '/eregulations/1002-Subpart-Interp/2016-16301')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/'
            '2016-07-11/interp-1/')

    def test_redirect_interp_section_past_lowercase(self):
        # troublemaker URL on launch day
        request = self.factory.get(
            '/eregulations/1002-subpart-interp/2011-31714')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/'
            '2011-12-30/interp-1/')

    def test_interp_section_current(self):
        request = self.factory.get(
            '/eregulations/1002-Subpart-Interp/2017-20417_20180101')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/interp-1/')

    def test_interp_section_no_subpart_with_default_section(self):
        # another launch troublemaker
        request = self.factory.get(
            '/eregulations/1005-Interp/2013-06861')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1005/'
            '2013-03-26/interp-2/')

    def test_redirect_no_pattern_match_after_part(self):
        """This tests our final fall-through redirect"""
        request = self.factory.get(
            '/eregulations/1002/9999/')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/')

    def test_get_version_date_bad_doc_number(self):
        part = '1002'
        doc = '2015-16301'
        self.assertIs(get_version_date(part, doc), None)
