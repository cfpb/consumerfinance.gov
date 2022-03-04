from django.core.files.base import ContentFile
from django.http import Http404, StreamingHttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import resolve, reverse

from wagtail.documents import get_document_model

from v1.views.documents import DocumentServeView


def create_document(filename):
    Document = get_document_model()
    document = Document(title="Test document")
    document.file.save(filename, ContentFile("Test content"))
    return document


class ServeViewTestCase(TestCase):
    def setUp(self):
        self.view = DocumentServeView()
        self.request = RequestFactory().get("/")

    def test_local_document_returns_file_contents(self):
        doc = create_document("test.txt")
        response = self.view.get(self.request, doc.pk, doc.filename)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, StreamingHttpResponse)
        self.assertEqual(b"".join(response.streaming_content), b"Test content")

    @override_settings(
        DEFAULT_FILE_STORAGE=(
            "wagtail.tests.dummy_external_storage.DummyExternalStorage"
        )
    )
    def test_external_document_uses_redirect(self):
        doc = create_document("test.txt")
        response = self.view.get(self.request, doc.pk, doc.filename)
        self.assertEqual(response.status_code, 302)

        # The redirect URL may or may not alter the original filename
        # depending on what else is stored in the dummy storage. If a file
        # named test.txt already exists, the filename will get 7 random
        # alphanumeric characters appended. See Django docs:
        # https://docs.djangoproject.com/en/stable/howto/custom-file-storage/#django.core.files.storage.get_available_name
        self.assertRegex(response["Location"], "/test(_[a-zA-Z0-9]{7})?.txt$")

    def test_missing_document_returns_404(self):
        with self.assertRaises(Http404):
            self.view.get(self.request, 9999, "missing.txt")


class ServeUrlTestCase(TestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse("wagtaildocs_serve", args=("123", "example.doc")),
            "/documents/123/example.doc",
        )

    def test_url_resolve(self):
        view = resolve("/documents/123/example.doc")
        self.assertEqual(view.func.__name__, "DocumentServeView")
