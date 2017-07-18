from django.apps import apps
from django.test import TestCase, override_settings

from v1.db_router import CFGOVRouter


class CFGOVRouterTestCase(TestCase):

    def setUp(self):
        self.router = CFGOVRouter()
        self.models = apps.get_app_config('v1').get_models()


@override_settings(DATABASES={'default': {}})
class CFGOVRouterNoReplicaTestCase(CFGOVRouterTestCase):

    def test_cfgov_apps_read_from_default_db(self):
        results = [self.router.db_for_read(m) == 'default'
                   for m in self.models]
        self.assertTrue(all(results))

    def test_cfgov_apps_write_to_default_db(self):
        results = [self.router.db_for_write(m) == 'default'
                   for m in self.models]
        self.assertTrue(all(results))

    def test_cfgov_apps_allow_migrate_default_db(self):
        self.assertTrue(self.router.allow_migrate('default', 'v1'))


@override_settings(DATABASES={'default': {}, 'replica': {}})
class CFGOVRouterReplicaTestCase(CFGOVRouterTestCase):

    def test_cfgov_apps_read_from_replica_db(self):
        results = [self.router.db_for_read(m) == 'replica'
                   for m in self.models]
        self.assertTrue(all(results))

    def test_cfgov_apps_write_to_default_db(self):
        results = [self.router.db_for_write(m) == 'default'
                   for m in self.models]
        self.assertTrue(all(results))

    def test_cfgov_apps_allow_migrate_default_db(self):
        self.assertTrue(self.router.allow_migrate('default', 'v1'))

    def test_cfgov_apps_disallow_migrate_replica_db(self):
        self.assertFalse(self.router.allow_migrate('replica', 'v1'))
