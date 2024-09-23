from django.apps import AppConfig
from django.conf import settings

import fs


class WagtailDeletionArchivalConfig(AppConfig):
    name = "wagtail_deletion_archival"
    label = "wagtail_deletion_archival"
    filesystem_name = getattr(
        settings, "WAGTAIL_DELETION_ARCHIVE_FILESYSTEM", None
    )
    filesystem = (
        fs.open_fs(filesystem_name) if filesystem_name is not None else None
    )
