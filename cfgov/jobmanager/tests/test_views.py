import django

from django.test import RequestFactory, TestCase
from mock import patch
from model_mommy import mommy

from flags.models import Flag
from jobmanager.models import Job
from jobmanager.views import (
    CurrentOpeningsView, FLAG_NAME, IndexView
)


django.setup()


class JobListViewTestCaseMixin(object):
    @classmethod
    def setUpClass(cls):
        super(JobListViewTestCaseMixin, cls).setUpClass()
        Flag.objects.get_or_create(
            key=FLAG_NAME,
            defaults={'enabled_by_default': True}
        )

    def setUp(self):
        self.view = self.view_cls()

    def request(self):
        request = RequestFactory().get('')
        return self.view_cls.as_view(flag_name=FLAG_NAME)(request)

    def mock_jobs(self, count):
        jobs = mommy.prepare(Job, _quantity=count) if count else []

        patched = patch(
            'jobmanager.views.JobListView.get_queryset',
            return_value=jobs
        )
        patched.start()
        self.addCleanup(patched.stop)

        return jobs

    def test_get(self):
        self.mock_jobs(100)
        self.assertEquals(self.request().status_code, 200)

    def test_get_no_jobs(self):
        self.mock_jobs(0)
        self.assertEquals(self.request().status_code, 200)


class IndexViewTestCase(JobListViewTestCaseMixin, TestCase):
    view_cls = IndexView

    def test_get_queryset_limits_max_results(self):
        limit = self.view.jobs_to_show
        jobs = self.mock_jobs(limit * 2)
        self.assertEqual(self.view.get_queryset(), jobs[:limit])


class CurrentOpeningsViewTestCase(JobListViewTestCaseMixin, TestCase):
    view_cls = CurrentOpeningsView
