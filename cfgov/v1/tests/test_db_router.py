from django.apps import apps
from django.test import TestCase, override_settings

from v1.db_router import CFGOVRouter


class CFGOVRouterTestCase(TestCase):

    def setUp(self):
        self.router = CFGOVRouter()
        self.v1_models = apps.get_app_config('v1').get_models()
        self.ask_models = apps.get_app_config('ask_cfpb').get_models()


@override_settings(DATABASES={'default': {}},
                   POSTGRES_APPS=['ask_cfpb'])
class CFGOVRouterNoPostgresTestCase(CFGOVRouterTestCase):

    def test_non_pg_apps_read_from_default_db(self):
        results = [self.router.db_for_read(m) == 'default'
                   for m in self.v1_models]
        self.assertTrue(all(results))

    def test_non_pg_apps_write_to_default_db(self):
        results = [self.router.db_for_write(m) == 'default'
                   for m in self.v1_models]
        self.assertTrue(all(results))

    def test_pg_apps_read_from_default_db(self):
        results = [self.router.db_for_read(m) == 'default'
                   for m in self.ask_models]
        self.assertTrue(all(results))

    def test_pg_apps_write_to_default_db(self):
        results = [self.router.db_for_write(m) == 'default'
                   for m in self.ask_models]
        self.assertTrue(all(results))

    def test_cfgov_apps_allow_migrate_default_db(self):
        self.assertTrue(self.router.allow_migrate('default', 'v1'))


@override_settings(DATABASES={'default': {}, 'postgres': {}},
                   POSTGRES_APPS=['ask_cfpb'])
class CFGOVRouterWithPostgresTestCase(CFGOVRouterTestCase):

    def test_non_pg_apps_read_from_default_db(self):
        results = [self.router.db_for_read(m) == 'default'
                   for m in self.v1_models]
        self.assertTrue(all(results))

    def test_non_pg_apps_write_to_default_db(self):
        results = [self.router.db_for_write(m) == 'default'
                   for m in self.v1_models]
        self.assertTrue(all(results))

    def test_pg_apps_read_from_pg_db(self):
        results = [self.router.db_for_read(m) == 'postgres'
                   for m in self.ask_models]
        self.assertTrue(all(results))

    def test_pg_apps_write_to_default_db(self):
        results = [self.router.db_for_write(m) == 'postgres'
                   for m in self.ask_models]
        self.assertTrue(all(results))

    def test_non_pg_apps_allow_migrate_default_db(self):
        self.assertTrue(self.router.allow_migrate('default', 'v1'))

    def test_pg_apps_disallow_migrate_replica_db(self):
        self.assertTrue(self.router.allow_migrate('postgres', 'v1'))
