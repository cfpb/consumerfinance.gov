from mock import Mock, patch

from django.core.files.base import ContentFile
from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.test import TestCase, override_settings
from wagtail.wagtaildocs.models import get_document_model

from v1.views.documents import DocumentServeView


def create_document(filename):
    Document = get_document_model()
    document = Document(title='Test document')
    document.file.save(filename, ContentFile('Some content'))
    return document


class ServeViewTestCase(TestCase):
    def setUp(self):
        self.view = DocumentServeView()
        self.request = Mock()

    def test_local_document_uses_wagtail_serve(self):
        filename = 'test.txt'
        doc = create_document(filename)

        with patch('v1.views.documents.wagtail_serve') as p:
            self.view.get(self.request, doc.pk, filename)
            p.assert_called_once_with(self.request, doc.pk, filename)

    @override_settings(
        AWS_QUERYSTRING_AUTH=False,
        AWS_STORAGE_BUCKET_NAME='test_s3_bucket',
        AWS_S3_CALLING_FORMAT='boto.s3.connection.OrdinaryCallingFormat',
        AWS_S3_SECURE_URLS=True,
        DEFAULT_FILE_STORAGE='v1.s3utils.MediaRootS3BotoStorage',
        MEDIA_URL='https://test.s3.amazonaws.com/f/',
        AWS_S3_ACCESS_KEY_ID='test-access-key',
        AWS_S3_SECRET_ACCESS_KEY='test-secret-access-key'
    )
    def test_document_serve_view_s3(self):
        filename = 'test.txt'
        with patch(
            'storages.backends.s3boto.S3BotoStorage._save',
            return_value=filename
        ):
            doc = create_document(filename)

        response = self.view.get(self.request, doc.pk, filename)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['Location'],
            'https://s3.amazonaws.com/test_s3_bucket/f/test.txt'
        )

    def test_missing_document_returns_404(self):
        with self.assertRaises(Http404):
            self.view.get(self.request, 9999, 'missing.txt')


class ServeUrlTestCase(TestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('wagtaildocs_serve', args=('123', 'example.doc')),
            '/documents/123/example.doc'
        )

    def test_url_resolve(self):
        view = resolve('/documents/123/example.doc')
        self.assertEqual(view.func.func_name, 'DocumentServeView')
