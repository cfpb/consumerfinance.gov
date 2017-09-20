import csv
from datetime import datetime

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseBadRequest

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from .models import CompanyInfo
from .forms import CompanyInfoForm


class Export(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "selfregistration.export"
    template_name = "selfregistration/export.html"

    def post(self, request):
        data = CompanyInfo.objects.all()
        if 'export_all' not in request.POST:
            data = data.filter(processed=False)

        # Create the HttpResponse object with the appropriate CSV header.
        now = datetime.now()
        response = HttpResponse(content_type='text/csv')
        export_filename = 'registrations-%s.csv' % now.strftime('%Y%m%d%I%M')
        disposition_header = 'attachment; filename="%s"' % export_filename
        response['Content-Disposition'] = disposition_header

        writer = csv.writer(response)
        writer.writerow(['id',
                         'company_name',
                         'address1',
                         'address2',
                         'city',
                         'state',
                         'zip',
                         'tax_id',
                         'website',
                         'company_phone',
                         'contact_name',
                         'contact_title',
                         'contact_email',
                         'contact_phone',
                         'contact_ext'])

        for row in data:
            writer.writerow([row.id,
                             row.company_name,
                             row.address1,
                             row.address2,
                             row.city,
                             row.state,
                             row.zip,
                             row.tax_id,
                             row.website,
                             row.company_phone,
                             row.contact_name,
                             row.contact_title,
                             row.contact_email,
                             row.contact_phone,
                             row.contact_ext])
        if 'mark_processed' in request.POST:
            data.update(processed=True)

        return response


class CompanySignup(FormView):
    template_name = 'selfregistration/register.html'
    form_class = CompanyInfoForm

    def form_valid(self, form):
        form.save()
        return HttpResponse('OK')

    def form_invalid(self, form):
        return HttpResponseBadRequest('Invalid Submission')
