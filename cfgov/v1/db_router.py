from django.conf import settings


class CFGOVRouter(object):
    """
    A router that allows for splitting reads and writes to separate
    databases.
    """

    def __init__(self, *args, **lwargs):
        self.has_postgres = 'postgres' in settings.DATABASES
        self.postgres_apps = getattr(settings, 'POSTGRES_APPS', [])

    def database_for_app(self, app_label):
        if self.has_postgres and app_label in self.postgres_apps:
            return 'postgres'

        else:
            return 'default'

    def db_for_read(self, model, **hints):
        """
        Send reads to the correct database
        """

        return self.database_for_app(model._meta.app_label)

    def db_for_write(self, model, **hints):
        """
        Send writes to the correct database
        """
        return self.database_for_app(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        """Disallow cross-database relationships"""
        obj1_db = self.database_for_app(obj1._meta.app_label)
        obj2_db = self.database_for_app(obj2._meta.app_label)
        return obj1_db == obj2_db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Always allow migrations (revist when we attempt replicas again)
        """
        return True
