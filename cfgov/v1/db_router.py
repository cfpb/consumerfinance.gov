from django.conf import settings


class CFGOVRouter(object):
    """
    A router that allows for splitting reads and writes to separate
    databases, and sends a set of legacy apps to a distinct 'legacy' DB
    """

    def __init__(self, *args, **lwargs):
        self.has_legacy = 'legacy' in settings.DATABASES
        self.has_replica = 'replica' in settings.DATABASES

    def model_is_legacy(self, model):
        return (model._meta.app_label in settings.LEGACY_APPS)

    def db_for_read(self, model, **hints):
        """
        if a 'legacy' DB exists, and this model is in settings.LEGACY_APPS,
        then all reads should go to 'legacy'

        Exceptions for authentication and user sessions
        """
        if self.model_is_legacy(model):
            return 'legacy'

        if self.has_replica and model._meta.app_label not in ('auth',
                                                              'sessions'):
            return 'replica'

        return 'default'

    def db_for_write(self, model, **hints):
        """
        if a 'legacy' DB exists, and this model is in settings.LEGACY_APPS,
        then all writes should go to 'legacy'

        Otherwise, all writes go to 'default'
        """
        if self.has_legacy and self.model_is_legacy(model):
            return 'legacy'

        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objs are legacy, or both aren't
        """
        if self.has_legacy:
            return not (self.model_is_legacy(obj1) ^
                        self.model_is_legacy(obj2))
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        allow legacy app migrations in the legacy DB, everything else in
        default
        """

        if self.has_legacy and app_label in settings.LEGACY_APPS:
            return db == 'legacy'
        else:
            return db == 'default'
