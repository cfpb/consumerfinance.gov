from core.services import PDFGeneratorView
from django.conf import settings
from django.http import HttpResponse
import six

if six.PY2:
    try:
        sys.path.append(os.environ.get('PDFREACTOR_LIB'))
        from PDFreactor import *
    except:
        PDFReactor = None


class HousingCounselorPDFView(PDFGeneratorView):
    def get_render_url(self):
        request = self.request
        api_url = 'hud-api-replace/%s.html/' % request.GET['zip']
        url = '%s://%s/%s' % (request.scheme, request.get_host(), api_url)
        return url

    def get(self, request):

        self.request = request
        return self.generate_pdf()

    def get_filename(self):
        return '%s.zip' % self.request.GET['zip']

    def generate_pdf(self):
        url = self.get_render_url()

        if self.license is None:
            raise Exception("PDFGeneratorView requires a license")

        try:
            pdf_reactor = PDFreactor()
        except:
            if settings.DEBUG:
                return HttpResponse("PDF Reactor is not configured, can not render %s" % self.get_render_url())
            else:
                raise PDFReactorNotConfigured('PDFreactor python library path needs to be configured.')

        pdf_reactor.setLogLevel(PDFreactor.LOG_LEVEL_WARN)
        pdf_reactor.setLicenseKey(str(self.license))
        pdf_reactor.setAuthor('CFPB')
        pdf_reactor.setAddTags(True)
        pdf_reactor.setAddBookmarks(True)

        result = pdf_reactor.renderDocumentFromURL(url)

        # Check if successful
        if result is None:
            # Not successful, return 500
            raise Exception('Error while rendering PDF: {}'.format(
                pdf_reactor.getError()))
        else:
            # Set the correct header for PDF output
            response = HttpResponse(result, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(
                self.get_filename())
            return response
