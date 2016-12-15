cfgov_apps = [
    'auth',
    'sessions',
    'admin',
    'contenttypes',
    'v1',
    'flags',
    'taggit',
    'jobmanager',
    'data_research'
]


class CFGOVRouter(object):
    """
    A router to control all database operations on models in
    wagtail and auth application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read cfgov-refresh models go to default.
        """
        if model._meta.app_label in cfgov_apps or model._meta.app_label.find('wagtail') != -1:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write cfgov-refresh models go to default.
        """
        if model._meta.app_label in cfgov_apps or model._meta.app_label.find('wagtail') != -1:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the cfgov-refresh app is involved.
        """
        if obj1._meta.app_label in cfgov_apps or obj2._meta.app_label in cfgov_apps or \
                        obj1._meta.app_label.find('wagtail') != -1 or obj2._meta.app_label.find('wagtail') != -1:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the cfgov-refresh app only appears in the 'default'
        database.
        """
        if app_label in cfgov_apps or app_label.find('wagtail') != -1:
            return db == 'default'
        return None


class LegacyRouter(object):
    def db_for_read(self, model, **hints):
        """
        All non cfgov-refresh Reads go to legacy Db.
        """
        return 'legacy'

    def db_for_write(self, model, **hints):
        """
        All non cfgov-refresh Writes always go to legacy Db.
        """
        return 'legacy'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the legacy db.
        """
        if obj1._state.db in 'legacy' and obj2._state.db in 'legacy':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non cfgov-refresh models end up in this pool.
        """
        return db == 'legacy'
