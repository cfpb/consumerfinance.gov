import os
from datetime import datetime, timezone
from urllib.parse import unquote

from django.conf import settings
from django.utils.encoding import smart_str

from wagtail.models import Page

from fs import copy, path
from wagtailbakery.views import WagtailBakeryView


class PageArchiveView(WagtailBakeryView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datetime = datetime.now(timezone.utc)

    def get_archive_path(self, obj):
        return f"{obj.slug}_{obj.pk}_{self.datetime.isoformat()}"

    def get_build_path(self, obj):
        # This is a wholesale rewrite of wagtail-bakery's get_build_path()
        # method that is more in line with django-bakery's get_build_path() in
        # that it uses self.fs instead of os to do filesystem operations,
        # making it easier to support non-OS filesystems.
        #
        # We could contribute this this upstream if we include multisite
        # support.

        url = self.get_url(obj)
        archive_path = self.get_archive_path(obj)
        page_path = unquote(url[1:])

        build_path = path.join(
            smart_str(settings.BUILD_DIR),
            archive_path,
            page_path,
        )

        self.fs.exists(build_path) or self.fs.makedirs(build_path)

        return path.join(build_path, "index.html")

    def get_queryset(self):
        return Page.objects.all().public()

    def build_media(self, obj):
        if os.path.exists(settings.MEDIA_ROOT) and settings.MEDIA_URL:
            archive_path = self.get_archive_path(obj)
            target_dir = path.join(
                smart_str(settings.BUILD_DIR),
                archive_path,
                settings.MEDIA_URL.lstrip("/"),
            )
            copy.copy_dir(
                "osfs:///",
                smart_str(settings.MEDIA_ROOT),
                self.fs,
                smart_str(target_dir),
            )

    def build_static(self, obj):
        if os.path.exists(settings.STATIC_ROOT) and settings.STATIC_URL:
            archive_path = self.get_archive_path(obj)
            target_dir = path.join(
                smart_str(settings.BUILD_DIR),
                archive_path,
                settings.STATIC_URL.lstrip("/"),
            )
            copy.copy_dir(
                "osfs:///",
                smart_str(settings.STATIC_ROOT),
                self.fs,
                smart_str(target_dir),
            )

    def build_archive(self, obj):
        self.build_media(obj)
        self.build_static(obj)
        self.build_object(obj)
