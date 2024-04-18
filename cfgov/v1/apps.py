from django.apps import AppConfig


class V1AppConfig(AppConfig):
    name = "v1"
    verbose_name = "V1"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import v1.signals  # noqa
