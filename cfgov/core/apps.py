from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'core'
    verbose_name = 'Core'

    def ready(self):
        # Import this module so that custom flag conditions are registered.
        import core.feature_flags  # noqa
