from django.apps import apps
from django.test import TestCase, override_settings

from v1.db_router import CFGOVRouter


def check_app_router(app, method_name):
    router = CFGOVRouter()
    method = getattr(router, method_name)

    models = apps.get_app_config(app).get_models()
    for model in models:
        return method(model)


@override_settings(LEGACY_APPS=['ask_cfpb'],
                   DATABASES={'default': {}, 'legacy': {}})
class CFGOVRouterNoReplicaTestCase(TestCase):

    def test_cfgov_apps_read_from_default_db(self):
        result = check_app_router('v1', 'db_for_read')
        self.assertEqual(result, 'default')

    def test_cfgov_apps_write_to_default_db(self):
        result = check_app_router('v1', 'db_for_write')
        self.assertEqual(result, 'default')

    def test_legacy_app_reads_routed_to_legacy(self):
        result = check_app_router('ask_cfpb', 'db_for_read')
        self.assertEqual(result, 'legacy')

    def test_legacy_app_writes_routed_to_legacy(self):
        result = check_app_router('ask_cfpb', 'db_for_write')
        self.assertEqual(result, 'legacy')


@override_settings(LEGACY_APPS=['ask_cfpb'],
                   DATABASES={'default': {}, 'legacy': {}, 'replica': {}})
class CFGOVRouterReplicaTestCase(TestCase):

    def test_cfgov_apps_read_from_replica_db(self):
        result = check_app_router('v1', 'db_for_read')
        self.assertEqual(result, 'replica')

    def test_cfgov_apps_write_to_default_db(self):
        result = check_app_router('v1', 'db_for_write')
        self.assertEqual(result, 'default')

    def test_legacy_app_reads_routed_to_legacy(self):
        result = check_app_router('ask_cfpb', 'db_for_read')
        self.assertEqual(result, 'legacy')

    def test_legacy_app_writes_routed_to_legacy(self):
        result = check_app_router('ask_cfpb', 'db_for_write')
        self.assertEqual(result, 'legacy')


@override_settings(LEGACY_APPS=['ask_cfpb'],
                   DATABASES={'default': {}})
class CFGOVRouterNoLegacyTestCase(TestCase):
    def test_legacy_app_reads_routed_to_default(self):
        result = check_app_router('ask_cfpb', 'db_for_read')
        self.assertEqual(result, 'default')

    def test_legacy_app_writes_routed_to_default(self):
        result = check_app_router('ask_cfpb', 'db_for_write')
        self.assertEqual(result, 'default')
