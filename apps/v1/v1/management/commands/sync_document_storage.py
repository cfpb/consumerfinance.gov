from django.core.management.base import BaseCommand

from wagtail.documents import get_document_model

from ._sync_storage_base import SyncStorageCommandMixin


class Command(SyncStorageCommandMixin, BaseCommand):
    def get_storage_directories(self):
        return ["documents"]

    def get_queryset(self):
        return get_document_model().objects.all()
