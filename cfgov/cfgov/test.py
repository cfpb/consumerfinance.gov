from __future__ import print_function

import importlib
import re

from django.apps import apps
from django.test.runner import DiscoverRunner


class TestDataTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        dbs = super(TestDataTestRunner, self).setup_databases(**kwargs)

        migration_methods = (
            (
                'wagtail.wagtailcore.migrations.0002_initial_data',
                'initial_data'
            ),
            (
                'wagtail.wagtailcore.migrations.0025_collection_initial_data',
                'initial_data'
            ),
            (
                'v1.migrations.0009_site_root_data',
                'create_site_root'
            ),
        )

        for migration, method in migration_methods:
            module = importlib.import_module(migration)
            getattr(module, method)(apps, None)

        return dbs


class HtmlMixin(object):
    def assertHtmlRegexpMatches(self, s, r):
        s_no_right_spaces = re.sub('>\s*', '>', s)
        s_no_left_spaces = re.sub('\s*<', '<', s_no_right_spaces)
        s_no_extra_spaces = re.sub('\s+', ' ', s_no_left_spaces)

        self.assertIsNotNone(
            re.search(r, s_no_extra_spaces.strip(), flags=re.DOTALL),
            '{} did not match {}'.format(s_no_extra_spaces, r)
        )
