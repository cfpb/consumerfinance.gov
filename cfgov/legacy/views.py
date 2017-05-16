import os
import re
import six
import sys

from django import http
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.services import PDFGeneratorView, PDFReactorNotConfigured
from v1.db_router import cfgov_apps

from .forms import HousingCounselorForm

if six.PY2:
    try:
        sys.path.append(os.environ.get('PDFREACTOR_LIB'))
        from PDFreactor import PDFreactor
    except:
        PDFreactor = None


class InvalidZipException(Exception):
    pass


class HousingCounselorView(TemplateView):
    template_name = 'find_a_housing_counselor.html'

    def get_context_data(self, **kwargs):
        context = super(HousingCounselorView, self).get_context_data(**kwargs)

        zipcode = self.request.GET.get('zipcode')
        context['zipcode'] = zipcode

        if zipcode:
            zipcode_valid = re.match(r'\d{5}', zipcode)
            context['zipcode_valid'] = zipcode_valid

            if zipcode_valid:
                context['counselors'] = self.get_counselors(zipcode)

        return context

    @staticmethod
    def get_counselors(zipcode):
        """Return list of housing counselors closest to a given zipcode.

        This could alternatively be an HTTP request to a django-hud API
        instance running locally.
        """
        from hud_api_replace.views import get_counsel_list
        response = get_counsel_list(zipcode, GET={})
        return response.get('counseling_agencies') or []


class HousingCounselorPDFView(PDFGeneratorView):
    def get_render_url(self):
        zip = self.form.cleaned_data['zip']
        api_url = 'hud-api-replace/%s.html/' % zip
        url = '%s://%s/%s' % ('http', 'localhost', api_url)
        return url

    def get(self, request):

        self.request = request
        self.form = HousingCounselorForm(request.GET)
        if not self.form.is_valid():
            return HttpResponse("That does not appear to be a valid zip code",
                                status=400)

        if settings.DEBUG and PDFreactor is None:
            return HttpResponse("PDF Reactor is not configured, "
                                "can not render %s" % self.get_render_url())

        return self.generate_pdf()

    def get_filename(self):
        return '%s.pdf' % self.request.GET['zip']

    def generate_pdf(self):
        url = self.get_render_url()

        if self.license is None:
            raise Exception("PDFGeneratorView requires a license")

        try:
            pdf_reactor = PDFreactor()
        except:
            raise PDFReactorNotConfigured('PDFreactor python library path '
                                          'needs to be configured.')

        pdf_reactor.setLogLevel(PDFreactor.LOG_LEVEL_FATAL)
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
            response['Content-Disposition'] = \
                'attachment; filename={0}'.format(self.get_filename())
            return response


def dbrouter_shortcut(request, content_type_id, object_id):
    """
    Redirect to an object's page based on a content-type ID and an object ID.
    """
    # Look up the object, making sure it's got a get_absolute_url() function.
    try:
        content_type = ContentType.objects.get(pk=content_type_id)
        if not content_type.model_class():
            raise http.Http404(
                _("Content type %(ct_id)s object has no associated model") %
                {'ct_id': content_type_id}
            )

        if content_type.app_label in cfgov_apps:
            obj = content_type.get_object_for_this_type(pk=object_id)
        else:
            obj = content_type.model_class().objects.db_manager(
                'legacy').get(pk=object_id)

    except (ObjectDoesNotExist, ValueError):
        raise http.Http404(
            _("Content type %(ct_id)s object %(obj_id)s doesn't exist") %
            {'ct_id': content_type_id, 'obj_id': object_id}
        )

    try:
        get_absolute_url = obj.get_absolute_url
    except AttributeError:
        raise http.Http404(
            _("%(ct_name)s objects don't have a get_absolute_url() method") %
            {'ct_name': content_type.name}
        )

    return http.HttpResponseRedirect(get_absolute_url())


@csrf_exempt
def token_provider(request):
    request.session.modified = True
    if request.method == 'POST':
        context = RequestContext(request)
        return render_to_response('common/csrf.html', context)
    return HttpResponse()
