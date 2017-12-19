import six

import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.views.generic.base import View


class PDFReactorNotConfigured(Exception):
    pass


# TODO: Update to python 3 when PDFreactor's python wrapper supports it.
if six.PY2:
    try:
        sys.path.append(os.environ.get('PDFREACTOR_LIB'))
        from PDFreactor import PDFreactor
    except:
        PDFreactor = None


class PDFGeneratorView(View):
    render_url = None
    stylesheet_url = None
    filename = None
    license = os.environ.get('PDFREACTOR_LICENSE')

    def get_render_url(self):
        if self.render_url is None:
            raise ImproperlyConfigured(
                "PDFGeneratorView requires either a definition of "
                "'render_url' or an implementation of 'get_render_url()'")
        return self.render_url

    def get_stylesheet_url(self):
        if self.stylesheet_url is None:
            raise ImproperlyConfigured(
                "PDFGeneratorView requires either a definition of "
                "'stylesheet_url' or an implementation of "
                "'get_stylesheet_url()'")
        return self.stylesheet_url

    def get_filename(self):
        if self.filename is None:
            raise ImproperlyConfigured(
                "PDFGeneratorView requires either a definition of "
                "'filename' or an implementation of 'get_filename()'")
        return self.filename

    def generate_pdf(self, query_opts):
        if self.license is None:
            raise Exception("PDFGeneratorView requires a license")

        if settings.DEBUG and PDFreactor is None:
            return HttpResponse("PDF Reactor is not configured, can not "
                                "render %s" % self.get_render_url())

        try:
            pdf_reactor = PDFreactor()
        except:
            raise PDFReactorNotConfigured('PDFreactor python library path '
                                          'needs to be configured.')

        pdf_reactor.setLogLevel(PDFreactor.LOG_LEVEL_WARN)
        pdf_reactor.setLicenseKey(str(self.license))
        pdf_reactor.setAuthor('CFPB')
        pdf_reactor.setAddTags(True)
        pdf_reactor.setAddBookmarks(True)
        pdf_reactor.addUserStyleSheet('', '', '', self.get_stylesheet_url())
        url = ('{0}?filter_calendar={1}&'
               'filter_range_date_gte={2}&'
               'filter_range_date_lte={3}'.format(
                   self.get_render_url(),
                   query_opts['filter_calendar'],
                   query_opts['filter_range_date_gte'],
                   query_opts['filter_range_date_lte']))

        result = pdf_reactor.renderDocumentFromURL(url)

        # Check if successful
        if result is None:
            # Not successful, return 500
            raise Exception('Error while rendering PDF: {}'.format(
                pdf_reactor.getError()))
        else:
            # Set the correct header for PDF output
            response = HttpResponse(result, content_type='application/pdf')
            response['Content-Disposition'] = \
                'attachment; filename={0}'.format(self.get_filename())
            return response
