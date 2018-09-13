from __future__ import unicode_literals

import datetime

from django.test import RequestFactory, TestCase, override_settings

from model_mommy import mommy

from regulations3k.models import EffectiveVersion, Part
from regulations3k.views import get_version_date, redirect_eregs


@override_settings(FLAGS={'REGULATIONS3K': {'boolean': 'True'}})
class RedirectRegulations3kTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.test_reg = mommy.make(
            Part,
            part_number='1002')

        self.test_version = mommy.make(
            EffectiveVersion,
            part=self.test_reg,
            effective_date=datetime.date(2016, 7, 11),
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
            '/eregulations/1002-1/2017-20417_20180101#1002-1')
        response = redirect_eregs(request)
        self.assertEqual(response.get('location'),
                         '/policy-compliance/rulemaking/regulations/1002/1/')

    def test_redirect_invalid_part(self):
        request = self.factory.get(
            '/eregulations/1020-1/2017-20417_20180101#1002-1')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/')

    def test_version_redirect(self):
        request = self.factory.get(
            '/eregulations/1002-1/2016-16301#1002-1')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/2016-07-11/1/')

    def test_version_redirect_no_version(self):
        request = self.factory.get(
            '/eregulations/1002-1/2011-31714#1002-1')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/1/')

    def test_search_redirect(self):
        request = self.factory.get(
            '/eregulations/search/1002',
            {'q': 'california', 'version': '2011-1'})
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/'
            'search-regulations/results/?regs=1002&q=california')

    def test_interp_appendix(self):
        request = self.factory.get(
            '/eregulations/1002-Appendices-Interp/'
            '2016-16301#1002-Interp-h1-1')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/')

    def test_interp_appendix_invalid_date(self):
        request = self.factory.get(
            '/eregulations/1024-Appendices-Interp/'
            '2017-20417_20180101#1002-Interp-h1-1')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1024/')

    def test_interp_intro(self):
        request = self.factory.get(
            '/eregulations/1002-Interp-h1/2016-16301#1030-Interp-h1')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/'
            '2016-07-11/h1-Interp/')

    def test_interp_intro_bad_version(self):
        request = self.factory.get(
            '/eregulations/1030-Interp-h1/2011-31727#1030-Interp-h1')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1030/Interp-0/')

    def test_interp_section_past(self):
        request = self.factory.get(
            '/eregulations/1002-Subpart-Interp/2016-16301')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/')

    def test_interp_section_current(self):
        request = self.factory.get(
            '/eregulations/1002-Subpart-Interp/'
            '2017-20417_20180101#1002-Subpart-Interp')
        response = redirect_eregs(request)
        self.assertEqual(
            response.get('location'),
            '/policy-compliance/rulemaking/regulations/1002/')

    def test_get_version_date_bad_doc_number(self):
        part = '1002'
        doc = '2015-16301'
        self.assertIs(get_version_date(part, doc), None)
