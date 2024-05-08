from django.apps import AppConfig
from django.conf import settings

import fs


class ArchivalConfig(AppConfig):
    name = "archival"
    label = "archival"
    filesystem_name = getattr(settings, "ARCHIVE_FILESYSTEM", "osfs:///")
    filesystem = fs.open_fs(filesystem_name)
