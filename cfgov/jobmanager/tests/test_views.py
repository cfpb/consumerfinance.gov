from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.test import RequestFactory, TestCase
from mock import patch
from model_mommy import mommy
from wagtail.wagtailcore.models import Site

from flags.models import Flag
from jobmanager.models import Job
from jobmanager.views import IndexView
from jobmanager.urls import FLAG_NAME
from scripts import create_careers_pages


class CareersViewTestCaseMixin(object):
    @classmethod
    def setUpClass(cls):
        super(CareersViewTestCaseMixin, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.site = Site.objects.get(is_default_site=True)

    @staticmethod
    def create_wagtail_careers_feature_flag(enabled):
        Flag.objects.create(key=FLAG_NAME, enabled_by_default=enabled)

    def request(self):
        path = reverse(self.url_name)
        request = self.factory.get(path)
        request.site = self.site
        resolved = resolve(path)
        return resolved.func(request)


class JobListViewTestCaseMixin(CareersViewTestCaseMixin):
    def mock_jobs(self, count):
        if count:
            jobs = mommy.make(Job, make_m2m=True, _quantity=count)
        else:
            jobs = []

        patched = patch(
            'jobmanager.views.JobListView.get_queryset',
            return_value=jobs
        )
        patched.start()
        self.addCleanup(patched.stop)

        return jobs

    def test_get(self):
        self.mock_jobs(10)
        self.assertEquals(self.request().status_code, 200)

    def test_get_no_jobs(self):
        self.mock_jobs(0)
        self.assertEquals(self.request().status_code, 200)

    def test_get_feature_flag_true(self):
        self.create_wagtail_careers_feature_flag(enabled=True)
        self.assertRaises(Http404, self.request)

    def test_get_feature_flag_false(self):
        self.create_wagtail_careers_feature_flag(enabled=False)
        self.assertEquals(self.request().status_code, 200)

    def test_get_wagtail_page(self):
        create_careers_pages.run()
        self.create_wagtail_careers_feature_flag(enabled=True)
        with patch(
            'transition_utilities.conditional_urls.wagtail_serve'
        ) as wagtail_serve:
            self.request()
            self.assertEqual(wagtail_serve.call_count, 1)


class IndexViewTestCase(JobListViewTestCaseMixin, TestCase):
    url_name = 'careers:jobs'

    def test_get_queryset_limits_max_results(self):
        view = IndexView()
        limit = view.jobs_to_show
        jobs = self.mock_jobs(limit * 2)
        self.assertEqual(view.get_queryset(), jobs[:limit])


class CurrentOpeningsViewTestCase(JobListViewTestCaseMixin, TestCase):
    url_name = 'careers:current_openings'
