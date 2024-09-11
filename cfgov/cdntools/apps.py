from django.apps import AppConfig


class CDNToolsAppConfig(AppConfig):
    name = "cdntools"
    label = "cdntools"
    verbose_name = "CDN Tools"

    def ready(self):
        import cdntools.signals  # noqa: F401
