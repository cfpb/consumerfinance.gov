from datetime import timedelta

from django.template import Context, Template
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.utils import dateparse, timezone

from flags.sources import get_flags


class TestCollectOutageBannerTag(SimpleTestCase):

    def render(self, path):
        request = RequestFactory().get(path)
        request.flag_conditions = get_flags()
        template = Template(
            '{% load banners %}'
            '{% collect_outage_banner request %}'
        )
        return template.render(Context({'request': request}))

    def test_banner_renders(self):
        response = self.render('/some/other/path/')
        self.assertIn('m-global-banner', response)


class TestComplaintIssueBannerTag(SimpleTestCase):

    def render(self, path):
        request = RequestFactory().get(path)
        request.flag_conditions = get_flags()
        template = Template(
            '{% load banners %}'
            '{% complaint_issue_banner request %}'
        )
        return template.render(Context({'request': request}))

    def test_banner_renders(self):
        response = self.render('/some/other/path/')
        self.assertIn('m-global-banner', response)


class TestComplaintMaintenanceBannerTag(SimpleTestCase):

    def render(self, path):
        request = RequestFactory().get(path)
        request.flag_conditions = get_flags()
        template = Template(
            '{% load banners %}'
            '{% complaint_maintenance_banner request %}'
        )
        return template.render(Context({'request': request}))

    @override_settings(FLAGS={'COMPLAINT_INTAKE_MAINTENANCE': [
        {
            'condition': 'before date',
            'value': dateparse.parse_datetime('2050-03-01T05:00Z'),
            'required': True
        },
    ]})
    def test_with_date_future(self):
        response = self.render('/no/pages/configured/')
        self.assertIn('m-global-banner', response)
        self.assertIn(
            'after 12:00 a.m. EST on Tuesday, March 1, 2050',
            response
        )

    @override_settings(FLAGS={'COMPLAINT_INTAKE_MAINTENANCE': [
        {
            'condition': 'before date',
            'value': '2050-03-01T05:00Z',
            'required': True
        },
    ]})
    def test_with_date_future_str(self):
        response = self.render('/no/pages/configured/')
        self.assertIn('m-global-banner', response)
        self.assertIn(
            'after 12:00 a.m. EST on Tuesday, March 1, 2050',
            response
        )

    @override_settings(FLAGS={'COMPLAINT_INTAKE_MAINTENANCE': [
        {
            'condition': 'before date',
            'value': timezone.now() - timedelta(days=1),
            'required': True
        },
    ]})
    def test_with_date_past(self):
        response = self.render('/no/pages/configured/')
        self.assertIn('m-global-banner', response)
        self.assertIn('soon', response)

    @override_settings(FLAGS={'COMPLAINT_INTAKE_MAINTENANCE': []})
    def test_without_dates(self):
        response = self.render('/page/configured/')
        self.assertIn('m-global-banner', response)
        self.assertIn('soon', response)


class TestOMWISalesforceOutageBannerTag(SimpleTestCase):

    def render(self, path):
        request = RequestFactory().get(path)
        request.flag_conditions = get_flags()
        template = Template(
            '{% load banners %}'
            '{% omwi_salesforce_outage_banner request %}'
        )
        return template.render(Context({'request': request}))

    def test_banner_renders(self):
        response = self.render('/some/other/path/')
        self.assertIn('m-global-banner', response)
