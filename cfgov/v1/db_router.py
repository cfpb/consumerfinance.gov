from django.conf import settings


class CFGOVRouter(object):
    """
    A router that allows for splitting reads and writes to separate
    databases.
    """

    def __init__(self, *args, **lwargs):
        self.has_replica = 'replica' in settings.DATABASES

    def db_for_read(self, model, **hints):
        """
        if a 'replica' DB exists and this model is not in the 'auth' or
        'sessions' app then all reads should go to the replica.
        """
        if self.has_replica and model._meta.app_label not in ('auth',
                                                              'sessions'):
            return 'replica'

        return 'default'

    def db_for_write(self, model, **hints):
        """
        All writes go to the default database
        """
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations only in the default database.
        """
        return db == 'default'
