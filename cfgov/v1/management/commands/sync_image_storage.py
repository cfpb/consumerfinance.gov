from django.core.management.base import BaseCommand

from wagtail.images import get_image_model

from ._sync_storage_base import SyncStorageCommandMixin


class Command(SyncStorageCommandMixin, BaseCommand):
    def get_storage_directories(self):
        return ["images", "original_images"]

    def get_queryset(self):
        return get_image_model().objects.all()

    def handle_instance(self, instance, log_prefix):
        super().handle_instance(instance, log_prefix)

        renditions = instance.renditions.all()
        rendition_count = renditions.count()

        for j, rendition in enumerate(renditions):
            rendition_prefix = "%d/%d (%d) " % (
                j + 1,
                rendition_count,
                rendition.pk,
            )
            self.stdout.write(log_prefix + rendition_prefix, ending="")
            self.save(rendition.file.name)
