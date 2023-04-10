from django.apps import AppConfig
from django.contrib.staticfiles import storage


class V1AppConfig(AppConfig):
    name = "v1"
    verbose_name = "V1"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        # Interesting situation: we use this pattern to account for
        # scrolling bugs in IE:
        # http://snipplr.com/view/518/
        # yet, url(null) trips up the ManifestStaticFilesStorage, so we
        # monkeypatch the regex so that url(null) is ignored
        storage.HashedFilesMixin.patterns = (
            (
                "*.css",
                (
                    r"""(url\((?!null)['"]{0,1}\s*(.*?)["']{0,1}\))""",
                    (
                        r"""(@import\s*["']\s*(.*?)["'])""",
                        """@import url("%s")""",
                    ),
                ),
            ),
        )
