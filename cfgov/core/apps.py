from django.apps import AppConfig

from core import checks  # noqa F401


class CoreAppConfig(AppConfig):
    name = "core"
    verbose_name = "Core"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        # Import this module so that custom flag conditions are registered.
        import core.feature_flags  # noqa
