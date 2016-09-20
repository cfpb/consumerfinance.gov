from django.apps import apps
from django.test import TestCase

from v1.db_router import CFGOVRouter, cfgov_apps


class CFGOVRouterTestCase(TestCase):
    def check_app_router(self, app, method_name, expected_db):
        router = CFGOVRouter()
        method = getattr(router, method_name)

        models = apps.get_app_config(app).get_models()
        for model in models:
            self.assertEqual(method(model), expected_db)

    def test_cfgov_apps_read_from_default_db(self):
        for app in cfgov_apps:
            self.check_app_router(app, 'db_for_read', 'default')

    def test_cfgov_apps_write_to_default_db(self):
        for app in cfgov_apps:
            self.check_app_router(app, 'db_for_write', 'default')

    def test_other_app_reads_are_not_routed(self):
        self.check_app_router('messages', 'db_for_read', None)

    def test_other_app_writes_are_not_routed(self):
        self.check_app_router('messages', 'db_for_write', None)
