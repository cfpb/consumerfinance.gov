import os
import re
import sys

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.functional import cached_property
from django.views.generic import TemplateView, View

import requests

from legacy.forms import HousingCounselorForm
from v1.s3utils import https_s3_url_prefix


class HousingCounselorView(TemplateView):
    def get_template_names(self):
        if 'pdf' in self.request.GET:
            return 'hud/housing_counselor_pdf.html'
        else:
            return 'hud/housing_counselor.html'

    def get_context_data(self, **kwargs):
        context = super(HousingCounselorView, self).get_context_data(**kwargs)
        context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN

        zipcode = self.request.GET.get('zipcode')
        context['zipcode'] = zipcode

        if zipcode:
            zipcode_valid = re.match(r'^\d{5}$', zipcode)

            if zipcode_valid:
                try:
                    api_json = self.get_counselors(self.request, zipcode)
                except requests.HTTPError:
                    pass
                else:
                    context.update({
                        'zipcode_valid': True,
                        'api_json': api_json,
                        'pdf_url': self.s3_pdf_url(zipcode),
                    })

        return context

    @classmethod
    def get_counselors(cls, request, zipcode):
        """Return list of housing counselors closest to a given zipcode.

        Raises requests.HTTPError on failure.
        """
        api_url = cls.s3_json_url(zipcode)

        response = requests.get(api_url)
        response.raise_for_status()

        return response.json()

    @staticmethod
    def s3_url(format, zipcode):
        path = settings.HOUSING_COUNSELOR_S3_PATH_TEMPLATE.format(
            format=format,
            zipcode=zipcode
        )
        return https_s3_url_prefix() + path

    @classmethod
    def s3_json_url(cls, zipcode):
        return cls.s3_url(format='json', zipcode=zipcode)

    @classmethod
    def s3_pdf_url(cls, zipcode):
        return cls.s3_url(format='pdf', zipcode=zipcode)


class HousingCounselorPDFView(View):
    def get(self, request):
        form = HousingCounselorForm(request.GET)

        if not form.is_valid():
            return HttpResponseBadRequest('invalid zip code')

        zipcode = form.cleaned_data['zip']
        render_url = self.get_render_url(zipcode)
        filename = '{}.pdf'.format(zipcode)

        return self.generate_pdf_from_url(render_url, filename)

    def get_render_url(self, zipcode):
        html_path = reverse('housing-counselor')
        return 'http://localhost{}?zipcode={}&pdf'.format(html_path, zipcode)

    def generate_pdf_from_url(self, url, filename):
        result = self.pdfreactor.renderDocumentFromURL(url)

        if result is None:
            raise Exception('Error while rendering PDF: {}'.format(
                self.pdfreactor.getError()
            ))

        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = \
            'attachment; filename={0}'.format(filename)
        return response

    @cached_property
    def pdfreactor(self):
        sys.path.append(os.environ['PDFREACTOR_LIB'])
        from PDFreactor import PDFreactor

        reactor = PDFreactor()

        reactor.setLogLevel(PDFreactor.LOG_LEVEL_FATAL)

        # License key needs to be cast to str here because PDFReactor
        # doesn't play well with unicode.
        reactor.setLicenseKey(str(os.environ['PDFREACTOR_LICENSE']))

        reactor.setAuthor('CFPB')
        reactor.setAddTags(True)
        reactor.setAddBookmarks(True)

        # Ensure that reactor can be connected to.
        try:
            reactor.renderDocumentFromContent('')
        except Exception:
            raise RuntimeError('Cannot connect to local PDFReactor')

        return reactor
