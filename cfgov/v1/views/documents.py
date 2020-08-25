from urllib.parse import urlparse

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View

from wagtail.documents import get_document_model
from wagtail.documents.views.serve import serve as wagtail_serve


class DocumentServeView(View):
    """Serve a non-local document by returning a redirect to its URL.

    Local files are served using the standard Wagtail document serve view.
    URL query string parameters are removed before the redirect is returned.
    """
    def get(self, request, document_id, document_filename):
        document = self.get_document_or_404(document_id)

        if self.is_local_file(document):
            return wagtail_serve(request, document_id, document_filename)
        else:
            return self.redirect_to_file_url(request, document)

    def get_document_or_404(self, document_id):
        Document = get_document_model()
        return get_object_or_404(Document, id=document_id)

    def is_local_file(self, document):
        try:
            return document.file.path
        except NotImplementedError:
            pass

    def redirect_to_file_url(self, request, document):
        url = self.remove_url_query_string(document.file.url)
        return redirect(url, permanent=False)

    @staticmethod
    def remove_url_query_string(url):
        parts = urlparse(url)
        return parts.scheme + '://' + parts.netloc + parts.path
