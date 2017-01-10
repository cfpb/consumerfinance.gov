from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.contrib.staticfiles import storage
from django.db.models.signals import post_save

from .signals import user_save_callback


class V1AppConfig(AppConfig):
    name = 'v1'
    verbose_name = 'V1'

    def ready(self):
        user_model = get_user_model()
        post_save.connect(user_save_callback, sender=user_model)
        # Interesting situation: we use this pattern to account for
        # scrolling bugs in IE:
        # http://snipplr.com/view/518/
        # yet, url(null) trips up the ManifestStaticFilesStorage, so we
        # monkeypatch the regex so that url(null) is ignored

        storage.HashedFilesMixin.patterns = (
            ("*.css", (
                r"""(url\((?!null)['"]{0,1}\s*(.*?)["']{0,1}\))""",
                (r"""(@import\s*["']\s*(.*?)["'])""", """@import url("%s")"""),
            )),
        )
