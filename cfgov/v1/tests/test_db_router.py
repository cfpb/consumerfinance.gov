from django.apps import apps
from django.test import TestCase, override_settings

from v1.db_router import CFGOVRouter


def check_app_router(app, method_name):
    router = CFGOVRouter()
    method = getattr(router, method_name)

    models = apps.get_app_config(app).get_models()
    for model in models:
        return method(model)


@override_settings(DATABASES={'default': {}})
class CFGOVRouterNoReplicaTestCase(TestCase):

    def test_cfgov_apps_read_from_default_db(self):
        result = check_app_router('v1', 'db_for_read')
        self.assertEqual(result, 'default')

    def test_cfgov_apps_write_to_default_db(self):
        result = check_app_router('v1', 'db_for_write')
        self.assertEqual(result, 'default')


@override_settings(DATABASES={'default': {}, 'replica': {}})
class CFGOVRouterReplicaTestCase(TestCase):

    def test_cfgov_apps_read_from_replica_db(self):
        result = check_app_router('v1', 'db_for_read')
        self.assertEqual(result, 'replica')

    def test_cfgov_apps_write_to_default_db(self):
        result = check_app_router('v1', 'db_for_write')
        self.assertEqual(result, 'default')
