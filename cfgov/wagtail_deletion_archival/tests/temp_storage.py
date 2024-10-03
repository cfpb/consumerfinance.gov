from tempfile import TemporaryDirectory

from django.test import override_settings
from django.test.utils import TestContextDecorator


class uses_temp_archive_storage(TestContextDecorator):
    def __init__(self):
        super().__init__(attr_name="temp_storage", kwarg_name="temp_storage")

    def enable(self):
        self.temp_storage = TemporaryDirectory()

        self.settings = override_settings(
            STORAGES={
                "wagtail_deletion_archival": {
                    "BACKEND": "django.core.files.storage.FileSystemStorage",
                    "OPTIONS": {
                        "location": self.temp_storage.name,
                    },
                }
            }
        )
        self.settings.enable()
        return self.temp_storage.name

    def disable(self):
        self.settings.disable()
        self.temp_storage.cleanup()
