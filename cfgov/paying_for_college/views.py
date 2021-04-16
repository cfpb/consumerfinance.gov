import json
import os
import re
from collections import OrderedDict

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import TemplateView, View

from paying_for_college.disclosures.scripts import nat_stats
from paying_for_college.forms import FeedbackForm
from paying_for_college.models import (
    ConstantCap, ConstantRate, Feedback, Notification, Program, School
)
from paying_for_college.models.search import SchoolSearch


BASEDIR = os.path.dirname(__file__)
DISCLOSURE_ROOT = 'paying-for-college2'
EXPENSE_FILE = '{}/fixtures/bls_data.json'.format(BASEDIR)
IPED_ERROR = "noSchool"
OID_ERROR = "noOffer"
PID_ERROR = "noProgram"


def get_json_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception:
        return ''


def validate_oid(oid):
    """
    Make sure an offer ID is valid according to our specifications.

    An offer ID can contain only case-insensitive hex values 0-9 and a-f
    and must be between 40 and 128 characters long.
    """
    find_illegal = re.search('[^0-9a-fA-F]+', oid)
    if find_illegal:
        return False
    else:
        if len(oid) >= 40 and len(oid) <= 128:
            return True
        else:
            return False


def validate_pid(pid):
    if not pid:
        return False
    for char in [';', '<', '>', '{', '}']:
        if char in pid:
            return False
    return True


def get_program_length(program, school):
    if program and program.level:
        LEVEL = program.level
    elif school and school.degrees_predominant:
        LEVEL = school.degrees_predominant
    elif school and school.degrees_highest:
        LEVEL = school.degrees_highest
    else:
        return None
    if LEVEL in ['0', '1', '2']:
        return 2
    elif LEVEL in ['3', '4']:
        return 4
    else:
        return None


def get_school(schoolID):
    """Try to get a school by ID; return either school or empty string"""
    try:
        school = School.objects.get(school_id=int(schoolID))
    except Exception:
        return None
    else:
        if school.operating is False:
            return None
        else:
            return school


def get_program(school, programCode):
    """Try to get latest program; return either program or empty string"""
    if not validate_pid(programCode):
        return None
    programs = Program.objects.filter(program_code=programCode,
                                      institution=school).order_by('-pk')
    if programs:
        return programs[0]
    else:
        return None


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)
        context['url_root'] = DISCLOSURE_ROOT
        return context


class OfferView(TemplateView):
    """consult values in querystring and deliver school/program data"""

    def get(self, request, test=False):
        school = None
        program = None
        program_data = 'null'
        school_data = 'null'
        warning = ''
        OID = ''
        if not request.GET:
            return render(request, 'paying_for_college/disclosure.html', {
                'data_js': "0",
                'school': school,
                'schoolData': school_data,
                'program': program,
                'programData': program_data,
                'oid': OID,
                'warning': warning,
                'url_root': DISCLOSURE_ROOT,
            })
        if 'oid' in request.GET and request.GET['oid']:
            OID = request.GET['oid']
        else:
            warning = OID_ERROR
        if OID and validate_oid(OID) is False:
            warning = OID_ERROR
            OID = ''
        if 'iped' in request.GET and request.GET['iped']:
            iped = request.GET['iped']
            school = get_school(iped)
            if school:
                school_data = school.as_json()
                if 'pid' in request.GET and request.GET['pid']:
                    PID = request.GET['pid']
                    if not validate_pid(PID):
                        warning = PID_ERROR
                        PID = ''
                    if PID:
                        programs = Program.objects.filter(
                            program_code=PID,
                            institution=school,
                            test=test).order_by('-pk')
                        if programs:
                            program = programs[0]
                            program_data = program.as_json()
                        else:
                            warning = PID_ERROR
                else:
                    warning = PID_ERROR
            else:
                warning = IPED_ERROR
        else:
            warning = IPED_ERROR
        return render(request, 'paying_for_college/disclosure.html', {
            'data_js': "0",
            'school': school,
            'schoolData': school_data,
            'program': program,
            'programData': program_data,
            'oid': OID,
            'warning': warning,
            'url_root': DISCLOSURE_ROOT,
        })


class FeedbackView(TemplateView):
    template_name = "paying-for-college/disclosure_feedback.html"

    @property
    def form(self):
        if self.request.method == 'GET':
            return FeedbackForm()

        elif self.request.method == 'POST':
            return FeedbackForm(self.request.POST)

    def get_context_data(self):
        cdict = dict(form=self.form)
        cdict['url_root'] = DISCLOSURE_ROOT
        return cdict

    def post(self, request):
        form = self.form
        if form.is_valid():
            feedback = Feedback(
                message=form.cleaned_data['message'][:2000],
                url=request.build_absolute_uri())
            feedback.save()
            return render(
                request,
                'paying-for-college/disclosure_feedback_thanks.html'
            )
        else:
            return HttpResponseBadRequest("Invalid form")


class SchoolRepresentation(View):

    def get_school(self, school_id):
        return get_object_or_404(School, pk=school_id)

    def get(self, request, school_id, **kwargs):
        school = self.get_school(school_id)
        return HttpResponse(school.as_json(), content_type='application/json')


class ProgramRepresentation(View):

    def get_program(self, program_code):
        ids = program_code.split('_')
        return Program.objects.filter(institution__school_id=int(ids[0]),
                                      program_code=ids[1]).first()

    def get(self, request, program_code, **kwargs):
        ids = program_code.split('_')
        if len(ids) != 2:
            format_error = ('Error: Programs must be specified in this way: '
                            '"/program/SCHOOLID_PROGRAMID/"')
            return HttpResponseBadRequest(format_error)
        PID = ids[1]
        if not validate_pid(PID):
            return HttpResponseBadRequest("Error: Invalid program ID")
        if not get_school(ids[0]):
            return HttpResponseBadRequest("Error: No school found")
        program = self.get_program(program_code)
        if not program:
            p_error = "Error: No program found"
            return HttpResponseBadRequest(p_error)
        return HttpResponse(program.as_json(),
                            content_type='application/json')


class StatsRepresentation(View):

    def get_stats(self, school, programID):
        program = get_program(school, programID)
        national_stats = nat_stats.get_prepped_stats(
            program_length=get_program_length(program, school)
        )
        return json.dumps(national_stats)

    def get(self, request, id_pair=''):
        school_id = id_pair.split('_')[0]
        school = get_school(school_id)
        try:
            program_id = id_pair.split('_')[1]
        except Exception:
            program_id = None
        stats = self.get_stats(school, program_id)
        return HttpResponse(stats, content_type='application/json')


class ExpenseRepresentation(View):
    """deliver BLS expense data in json form"""

    def get(self, request):
        expense_json = get_json_file(EXPENSE_FILE)
        if not expense_json:
            error = "No expense data could be found"
            return HttpResponseBadRequest(error)
        return HttpResponse(expense_json, content_type='application/json')


class ConstantsRepresentation(View):
    """deliver stored Constants in json form"""

    def get_constants(self):
        constants = OrderedDict()
        for ccap in ConstantCap.objects.order_by('slug'):
            constants[ccap.slug] = ccap.value
        for crate in ConstantRate.objects.order_by('slug'):
            constants[crate.slug] = "{0}".format(crate.value)
        cy = constants['constantsYear']
        constants['constantsYear'] = "{}-{}".format(cy, str(cy + 1)[2:])
        return json.dumps(constants)

    def get(self, request):
        return HttpResponse(self.get_constants(),
                            content_type='application/json')


def school_autocomplete(request):
    document = []
    search_term = request.GET.get('q', '').strip()
    if search_term:
        response = SchoolSearch(search_term).autocomplete()

        document = [{'schoolname': school.text,
                     'id': school.school_id,
                     'city': school.city,
                     'nicknames': school.nicknames,
                     'state': school.state,
                     'zip5': school.zip5,
                     'url': school.url}
                    for school in response.get('results')]

    return JsonResponse(document, safe=False)


class VerifyView(View):
    def post(self, request):
        data = request.POST
        timestamp = timezone.now()
        if data.get('oid') and validate_oid(data['oid']):
            OID = data['oid']
        else:
            return HttpResponseBadRequest('Error: No valid OID provided')
        if data.get('iped') and get_school(data['iped']):
            school = get_school(data['iped'])
            if not school.contact:
                errmsg = "Error: School has no contact."
                return HttpResponseBadRequest(errmsg)
            if Notification.objects.filter(institution=school, oid=OID):
                errmsg = "Error: OfferID has already generated a notification."
                return HttpResponseBadRequest(errmsg)
            notification = Notification(
                institution=school,
                oid=OID,
                url=data['URL'].replace('#info-right', ''),
                timestamp=timestamp,
                errors=data['errors'][:255])
            notification.save()
            msg = notification.notify_school()
            callback = json.dumps({'result':
                                   'Verification recorded; {0}'.format(msg)})
            response = HttpResponse(callback)
            return response
        else:
            errmsg = ("Error: No school found")
            return HttpResponseBadRequest(errmsg)
