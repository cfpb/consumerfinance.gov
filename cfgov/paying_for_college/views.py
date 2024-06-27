import json
import os
import re
from collections import OrderedDict

from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import TemplateView, View

from paying_for_college.disclosures.scripts import nat_stats
from paying_for_college.models import (
    ConstantCap,
    ConstantRate,
    Notification,
    Program,
    School,
)
from paying_for_college.models.search import SchoolSearch


BASEDIR = os.path.dirname(__file__)
DISCLOSURE_ROOT = "paying-for-college2"
EXPECTED_ERROR_MESSAGES = [
    "none",
    "INVALID: student indicated the offer information is wrong",
]
EXPENSE_FILE = f"{BASEDIR}/fixtures/bls_data.json"
IPED_ERROR = "noSchool"
OID_ERROR = "noOffer"
PID_ERROR = "noProgram"


def get_json_file(filename):
    try:
        with open(filename) as f:
            return f.read()
    except Exception:
        return ""


def validate_oid(oid):
    """
    Make sure an offer ID is valid according to our specifications.

    An offer ID can contain only case-insensitive hex values 0-9 and a-f
    and must be between 40 and 128 characters long.
    """
    find_illegal = re.search("[^0-9a-fA-F]+", oid)
    if find_illegal:
        return False
    else:
        return bool(len(oid) >= 40 and len(oid) <= 128)


def validate_pid(pid):
    if not pid:
        return False
    return all(char not in pid for char in [";", "<", ">", "{", "}", "_"])


def url_is_safe(url):
    """Only save disclosure URLs with expected values."""
    find_illegal = re.search("[^0-9a-zA-Z-/?&=:.#]+", url)
    return find_illegal is None


def get_program_length(program, school):
    if program and program.level:
        LEVEL = program.level
    elif school and school.degrees_predominant:
        LEVEL = school.degrees_predominant
    elif school and school.degrees_highest:
        LEVEL = school.degrees_highest
    else:
        return None
    if LEVEL in ["0", "1", "2"]:
        return 2
    elif LEVEL in ["3", "4"]:
        return 4
    else:
        return None


def get_school(schoolID):
    """Try to get a school by ID; return either school or empty string."""
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
    """Try to get latest program; return either program or empty string."""
    if not validate_pid(programCode):
        return None
    programs = Program.objects.filter(
        program_code=programCode, institution=school
    ).order_by("-pk")
    if programs:
        return programs[0]
    else:
        return None


def format_constants():
    constants = {}
    rates = ConstantRate.objects.all()
    caps = ConstantCap.objects.all()
    for rate in rates:
        constants[rate.slug] = f"{round((rate.value * 100), 3).normalize()}%"
    for cap in caps:
        if cap.slug == "constantsYear":
            year_value = f"{cap.value}-" + f"{cap.value + 1}"[-2:]
            constants[cap.slug] = year_value
        else:
            constants[cap.slug] = f"${cap.value:,}"
    return constants


class BaseTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url_root"] = DISCLOSURE_ROOT
        context.update(format_constants())
        return context


class OfferView(TemplateView):
    """Consult values in querystring and deliver school/program data."""

    def get(self, request, test=False):
        school = None
        program = None
        program_data = "null"
        school_data = "null"
        warning = ""
        OID = ""
        if not request.GET:
            raise Http404
        if "oid" in request.GET and request.GET["oid"]:
            OID = request.GET["oid"]
        else:
            warning = OID_ERROR
        if OID and validate_oid(OID) is False:
            warning = OID_ERROR
            OID = ""
        school_id = request.GET.get("iped", "")
        if school_id and str(school_id).isdigit():
            school = get_school(school_id)
            if school:
                school_data = school.as_json()
                PID = request.GET.get("pid")
                if not validate_pid(PID):
                    warning = PID_ERROR
                    PID = ""
                if PID:
                    programs = Program.objects.filter(
                        program_code=PID, institution=school, test=test
                    ).order_by("-pk")
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
        return render(
            request,
            "paying-for-college/disclosure.html",
            {
                "data_js": "0",
                "school": school,
                "schoolData": school_data,
                "program": program,
                "programData": program_data,
                "oid": OID,
                "warning": warning,
                "url_root": DISCLOSURE_ROOT,
            },
        )


class SchoolRepresentation(View):
    def get_school(self, school_id):
        return get_object_or_404(School, pk=school_id)

    def get(self, request, school_id, **kwargs):
        school = self.get_school(school_id)
        return HttpResponse(school.as_json(), content_type="application/json")


class ProgramRepresentation(View):
    def get_program(self, program_code):
        ids = program_code.split("_")
        return Program.objects.filter(
            institution__school_id=int(ids[0]), program_code=ids[1]
        ).first()

    def get(self, request, program_code, **kwargs):
        ids = program_code.split("_")
        if len(ids) != 2:
            format_error = (
                "Error: Programs must be specified in this way: "
                '"/program/SCHOOLID_PROGRAMID/"'
            )
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
        return HttpResponse(program.as_json(), content_type="application/json")


class StatsRepresentation(View):
    def get_stats(self, school, programID):
        program = get_program(school, programID)
        national_stats = nat_stats.get_prepped_stats(
            program_length=get_program_length(program, school)
        )
        return json.dumps(national_stats)

    def get(self, request, id_pair=""):
        school_id = id_pair.split("_")[0]
        school = get_school(school_id)
        try:
            program_id = id_pair.split("_")[1]
        except Exception:
            program_id = None
        stats = self.get_stats(school, program_id)
        return HttpResponse(stats, content_type="application/json")


class ExpenseRepresentation(View):
    """Deliver BLS expense data in json form."""

    def get(self, request):
        expense_json = get_json_file(EXPENSE_FILE)
        if not expense_json:
            error = "No expense data could be found"
            return HttpResponseBadRequest(error)
        return HttpResponse(expense_json, content_type="application/json")


class ConstantsRepresentation(View):
    """Deliver stored Constants in json form."""

    def get_constants(self):
        constants = OrderedDict()
        for ccap in ConstantCap.objects.order_by("slug"):
            constants[ccap.slug] = ccap.value
        for crate in ConstantRate.objects.order_by("slug"):
            constants[crate.slug] = f"{crate.value}"
        cy = constants["constantsYear"]
        constants["constantsYear"] = f"{cy}-{str(cy + 1)[2:]}"
        return json.dumps(constants)

    def get(self, request):
        return HttpResponse(
            self.get_constants(), content_type="application/json"
        )


def school_autocomplete(request):
    document = []
    search_term = request.GET.get("q", "").strip()
    if search_term:
        response = SchoolSearch(search_term).autocomplete()

        document = [
            {
                "schoolname": school.text,
                "id": school.school_id,
                "city": school.city,
                "nicknames": school.nicknames,
                "state": school.state,
                "zip5": school.zip5,
                "url": school.url,
            }
            for school in response.get("results")
        ]

    return JsonResponse(document, safe=False)


class VerifyView(View):
    def post(self, request):
        data = json.loads(request.body)
        timestamp = timezone.now()
        OID = data.get("oid")
        if OID and validate_oid(OID):
            pass
        else:
            return HttpResponseBadRequest("Error: No valid OID provided")
        iped = data.get("iped")
        if iped and str(iped).isdigit():
            school = get_school(iped)
            if not school:
                errmsg = "Error: No school found."
                return HttpResponseBadRequest(errmsg)
            if not school.contact:
                errmsg = "Error: School has no contact."
                return HttpResponseBadRequest(errmsg)
            if Notification.objects.filter(institution=school, oid=OID):
                errmsg = "Error: OfferID has already generated a notification."
                return HttpResponseBadRequest(errmsg)
            raw_url = data.get("URL")
            if url_is_safe(raw_url):
                url = raw_url.replace("#info-right", "")
            else:
                url = "Unsafe URL found for {OID}"
            errors = data["errors"]
            if errors not in EXPECTED_ERROR_MESSAGES:
                errors = "App delivered unexpected error for {OID}"
            notification = Notification(
                institution=school,
                oid=OID,
                url=url,
                timestamp=timestamp,
                errors=errors,
            )
            notification.save()
            msg = notification.notify_school()
            callback = json.dumps({"result": f"Verification recorded; {msg}"})
            response = HttpResponse(callback)
            return response
        else:
            errmsg = "Error: No valid school ID found"
            return HttpResponseBadRequest(errmsg)
