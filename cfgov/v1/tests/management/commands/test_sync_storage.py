import os.path
import re
import tempfile
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from wagtail.documents import get_document_model
from wagtail.documents.tests.utils import get_test_document_file
from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file

import responses


class SyncStorageTestMixin:
    def setUp(self):
        self.fake_storage = "https://example-cfpbtest.gov/files/"
        responses.add(responses.GET, re.compile(self.fake_storage + r".*"))

        self.tempdir = tempfile.TemporaryDirectory()

    @responses.activate
    def test_sync(self):
        out = StringIO()

        call_command(
            self.sync_command,
            self.fake_storage,
            self.tempdir.name + "/",
            stdout=out,
        )

        for instance in self.model_cls.objects.all():
            synced_filename = os.path.join(
                self.tempdir.name, instance.file.name
            )
            self.assertTrue(os.path.exists(synced_filename))


class SyncDocumentStorageTests(SyncStorageTestMixin, TestCase):
    def setUp(self):
        super().setUp()

        # Create some test documents in the database.
        Document = get_document_model()

        for _ in range(3):
            document = Document(title="test")
            document.file.save("testing.txt", get_test_document_file())

        self.model_cls = Document
        self.sync_command = "sync_document_storage"


class SyncImageStorageTests(SyncStorageTestMixin, TestCase):
    def setUp(self):
        super().setUp()

        # Create some test images in the database.
        Image = get_image_model()

        for _ in range(3):
            image = Image.objects.create(
                title="testing",
                file=get_test_image_file(),
            )
            image.get_rendition("original")

        self.model_cls = Image
        self.sync_command = "sync_image_storage"
