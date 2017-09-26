from __future__ import unicode_literals
# import unittest

import django
# import mock

from data_research.scripts.pipeline import check_for_data_updates


class PipelineTests(django.test.TestCase):

    def test_check_for_data_updates(self):
        msg = check_for_data_updates()
        self.assertIn('No new' in msg)
