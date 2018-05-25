from unittest import TestCase

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtaildocs.models import Document

import boto
import moto

from v1.storage import OverwritingS3Storage


@override_settings(
    DEFAULT_FILE_STORAGE='v1.storage.OverwritingS3Storage'
)
class TestOverwritingS3Storage(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        mock_s3 = moto.mock_s3_deprecated()
        mock_s3.start()
        self.addCleanup(mock_s3.stop)

        self.s3 = boto.connect_s3()
        self.s3.create_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    def test_replace_deletes_old_file(self):
        f = SimpleUploadedFile('test.txt', 'Original')
        doc = Document.objects.create(title='Test document', file=f)

        storage = doc.file.storage
        old_storage_filename = doc.file.name
       
        self.client.post(
            reverse('wagtaildocs:edit', args=(doc.pk,)),
            {
                'title': 'Different file',
                'file': SimpleUploadedFile('test2.txt', 'Different'),
            }
        )

        doc.refresh_from_db()
        self.assertTrue(storage.exists(doc.file.name))
        self.assertFalse(storage.exists(old_storage_filename))

    def test_overwrite_file(self):
        f = SimpleUploadedFile('test.txt', 'Original')
        doc = Document.objects.create(title='Test document', file=f)

        self.client.post(
            reverse('wagtaildocs:edit', args=(doc.pk,)),
            {
                'title': 'Overwritten',
                'file': SimpleUploadedFile('test.txt', 'Overwritten'),
            }
        )

        doc.refresh_from_db()
        stored_content = doc.file.storage.open(doc.file.name).read()
        self.assertEqual(stored_content, 'Overwritten')

    def test_delete_file_works_properly(self):
        f = SimpleUploadedFile('test.txt', 'Original')
        doc = Document.objects.create(title='Test document', file=f)

        self.client.post(
            reverse('wagtaildocs:delete', args=(doc.pk,)),
        )

        with self.assertRaises(Document.DoesNotExist):
            doc.refresh_from_db()
