import datetime
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from jobmanager import views, models
import random
import re
import string


class JobTest(TestCase):
    def random_string(self, length):
        return ''.join(random.choice(string.lowercase + string.digits)
                for x in range(length))

    def job_factory(self, **kwargs):
        """
        Create a job with some defaults.
        """
        cat = models.JobCategory(slug=self.random_string(10), 
                job_category='Test', active=True)
        cat.save()
        today = datetime.date.today()
        args = {'slug': self.random_string(10), 'title': 'Example', 
                'category': cat, 'description': 'Foo bar',
                'open_date': today, 'close_date': today}
        for key in kwargs:
            args[key] = kwargs[key]
        job = models.Job(**args)
        job.save()
        return job

    def test_jobs(self):
        """
        Passthrough to the jobs_update template.
        """
        response = views.jobs(RequestFactory().get('/'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jobs" in response.content)
        self.assertTrue(len(response.content) > 2000)
    
    def test_detail_day(self):
        """
        Test job match by day.
        """
        #   Create possible combinations
        cat = models.JobCategory(slug='tst', job_category='Test', 
                active=True)
        cat.save()
        def createJob(delta_open, delta_closed):
            open = datetime.date.today() +\
                datetime.timedelta(days=delta_open)
            closed = datetime.date.today() +\
                datetime.timedelta(days=delta_closed)

            models.Job(slug=str(delta_open) + str(delta_closed), 
                    title='Test', category=cat, open_date=open,
                    close_date=closed).save()
        for o in range(-1,2):
            for c in range(-1,2):
                createJob(o, c)
        
        #   Now, we should only see the entries in the correct range
        four_oh_four = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1)]
        success = [(-1,0), (-1,1), (0,0), (0,1)]
        for (o,c) in four_oh_four:
            self.assertRaises(Http404, views.detail,
                RequestFactory().get('/'), str(o) + str(c))
        for (o,c) in success:
            response = views.detail(RequestFactory().get('/'), 
                    str(o) + str(c))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Test" in response.content)

    def test_detail_slug_active(self):
        """
        Tests job match by slug and active status.
        """
        job = self.job_factory()

        #   Success
        response = views.detail(RequestFactory().get('/'), job.slug)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(job.title in response.content)

        #   Failure due to slug
        job.slug='ex'
        job.save()
        self.assertRaises(Http404, views.detail, 
                RequestFactory().get('/'), 'example')

        #   Failure due to active status
        job.slug='example'
        job.active=False
        self.assertRaises(Http404, views.detail, 
                RequestFactory().get('/'), 'example')
    
    def test_detail_content(self):
        """
        Verifies the content of the page is what's expected.
        """
        cat = models.JobCategory(slug='tst', job_category='TestCat', 
                active=True)
        grade_low = models.Grade(slug='low', grade='LowLowLow',
                salary_min=44000, salary_max=48000)
        grade_high = models.Grade(slug='high', grade='HighHighHigh',
                salary_min=45000, salary_max=50000)
        location_a = models.Location(slug='chitown',
                description='Chi-Town', region='IL',
                region_long='ILLLL')
        location_b = models.Location(slug='bigben',
                description='Big Ben', region='UK',
                region_long='U.K.')
        for model in (cat,grade_low,grade_high,location_a,location_b):
            model.save()

        today = datetime.date.today()
        job = models.Job(slug='aaaaaa', title='BBBBBB',
                description='cccccc', category=cat, salary_min=500,
                salary_max=600, open_date=today, close_date=today)
        job.save()
        job.grades.add(grade_low)
        job.grades.add(grade_high)
        job.locations.add(location_a)
        job.locations.add(location_b)
        job.save()

        response = views.detail(RequestFactory().get('/'), 'aaaaaa')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("BBBBBB" in response.content)
        self.assertTrue("cccccc" in response.content)
        self.assertTrue("TestCat" in response.content)
        self.assertTrue("ILLLL" in response.content)
        self.assertTrue("U.K." in response.content)
        self.assertTrue("LowLowLow" in response.content)
        self.assertTrue("HighHighHigh" in response.content)
        #   If salary_min and salary_max are present, it shows them
        self.assertTrue("500" in response.content)
        self.assertTrue("600" in response.content)
        #   If they are not present, the grade's pay is used
        job.salary_min = None
        job.salary_max = None
        job.save()
        response = views.detail(RequestFactory().get('/'), 'aaaaaa')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("44,000" in response.content)
        self.assertTrue("50,000" in response.content)
    
    def test_detail_referrer(self):
        """
        Test the referrerer adds the breadcrumb. The breadcrumb logic
        is a little strange; it cuts out the domain and the first
        directory.
        """
        job = self.job_factory()
        request = RequestFactory().get('/')
        request.META['HTTP_REFERER'] = 'http://e.com/some/pathtoplace'
        response = views.detail(request, job.slug)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('/jobs/pathtoplace' in response.content)
        self.assertTrue('>pathtoplace<' in response.content)

        #   Also test that it works with no referrer
        job = self.job_factory()
        response = views.detail(RequestFactory().get('/'), job.slug)

        self.assertEqual(response.status_code, 200)
        self.assertFalse('>None</a>' in response.content)
        self.assertTrue('/jobs/location' in response.content)
        self.assertTrue('>location<' in response.content)

    def test_open_graph_title_default(self):
        job = self.job_factory()

        self.assertEqual(job.title, job.get_open_graph_title())

    def test_open_graph_title_custom(self):
        job = self.job_factory()
        job.open_graph_title = 'My custom title'
        job.save()

        self.assertEqual(job.get_open_graph_title(), 'My custom title')

    def test_open_graph_description_default(self):
        job = self.job_factory()

        self.assertIn(job.get_open_graph_description(), job.description)

    def test_open_graph_description_custom(self):
        job = self.job_factory()
        job.open_graph_description = 'My custom description'
        job.save()

        self.assertEqual(job.get_open_graph_description(),
            'My custom description')

    def test_tweet_text_default(self):
        job = self.job_factory()

        self.assertEqual(job.title, job.get_twitter_text())

    def test_tweet_text_custom(self):
        job = self.job_factory()
        job.twitter_text = 'Our tweets are the best'
        job.save()

        self.assertEqual(job.get_twitter_text(), 'Our tweets are the best')

    def test_utm_campaign_absent(self):
        job = self.job_factory()

        resp = self.client.get(job.get_absolute_url())
        
        self.assertNotIn('utm_campaign', resp.content)

    def test_utm_campaign_present(self):
        job = self.job_factory()
        job.utm_campaign = 'jobblitz'
        job.save()

        resp = self.client.get(job.get_absolute_url())

        self.assertIn('utm_campaign=jobblitz', resp.content)
