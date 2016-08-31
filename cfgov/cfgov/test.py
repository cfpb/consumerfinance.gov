from __future__ import print_function

import importlib
import re

from django.apps import apps
from django.test.runner import DiscoverRunner
from wagtail.wagtailcore.models import Page

from scripts import initial_data


class TestDataTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        dbs = super(TestDataTestRunner, self).setup_databases(**kwargs)

        if not self.check_for_wagtail_root():
            self.setup_wagtail_root()

        initial_data.run()
        return dbs

    def check_for_wagtail_root(self):
        return Page.objects.filter(slug='root').exists()

    def setup_wagtail_root(self):
        migration = 'wagtail.wagtailcore.migrations.0002_initial_data'
        print('Running migration {} to setup Wagtail root'.format(migration))

        module = importlib.import_module(migration)
        module.initial_data(apps, None)


class HtmlMixin(object):
    def assertHtmlRegexpMatches(self, s, r):
        s_no_right_spaces = re.sub('>\s*', '>', s)
        s_no_left_spaces = re.sub('\s*([<"])', r'\1', s_no_right_spaces)
        s_no_extra_spaces = re.sub('\s+', ' ', s_no_left_spaces)

        self.assertIsNotNone(
            re.search(r, s_no_extra_spaces.strip(), flags=re.DOTALL),
            '{} did not match {}'.format(s_no_extra_spaces, r)
        )
