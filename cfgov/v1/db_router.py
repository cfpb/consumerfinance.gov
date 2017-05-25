from django.conf import settings

legacy_apps = [
    'comparisontool',
    'paying_for_college',
    'retirement_api',
    'knowledgebase',
    'agreements',
    'picard'
    'regcore',
]


class CFGOVRouter(object):
    """
    A router that allows for splitting reads and writes to seperate
    databases, and sends a set of legacy apps to a distinct 'legacy' DB
    """

    has_legacy = 'legacy' in settings.DATABASES
    has_replica = 'replica' in settings.DATABASES

    def model_is_legacy(self, model):
        return (model._meta.app_label in legacy_apps)

    def db_for_read(self, model, **hints):
        """
        if a 'legacy' DB exists, and this model is in legacy_apps, then
        all reads should go to 'legacy'

        Otherwise, if a 'replica' DB exists, send reads there. Failing that
        returns 'default'
        """
        if self.has_legacy and self.model_is_legacy(model):
            return 'legacy'
        if self.has_replica:
            return 'replica'

        return 'default'

    def db_for_write(self, model, **hints):
        """
        if a 'legacy' DB exists, and this model is in legacy_apps, then
        all writes should go to 'legacy'

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

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        allow legacy app migrations in the legacy DB, everything else in
        default
        """
        if self.has_legacy and app_label in legacy_apps:
            return db == 'legacy'

        else:
            return db == 'default'
