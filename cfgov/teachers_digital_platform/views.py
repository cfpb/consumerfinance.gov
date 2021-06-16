import re
import time

from typing import Dict

from django.core import signing
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse

from formtools.wizard.views import NamedUrlCookieWizardView

from .assessments import (
    Question, available_assessments, get_assessment, get_form_lists)
from . import urlEncode


signer = signing.Signer()


class AssessmentWizard(NamedUrlCookieWizardView):
    def done(self, form_list, **kwargs):
        # Find assessment based on hidden "_k" question in page1
        first_page = self.get_form('page1')
        assessment_key = first_page.fields['_k'].initial
        if (not isinstance(assessment_key, str) or
                assessment_key not in available_assessments):
            # Hmm this isn't right
            response = HttpResponseRedirect('../')
            response.delete_cookie('resultUrl')
            response.delete_cookie('wizard_survey_wizard')
            return response

        assessment = get_assessment(assessment_key)

        # Calc score and encode in URL
        question_scores: Dict[Question, float] = assessment.get_score(
            self.get_all_cleaned_data())['question_scores']
        part_scores: Dict[str, float] = {}

        for question, score in question_scores.items():
            part = re.match(r'^\d+', question.section)[0]
            if part not in part_scores:
                part_scores[part] = 0
            part_scores[part] += score

        subtotals = (v for k, v in sorted(part_scores.items()))
        encoded = urlEncode.dumps(assessment, subtotals, time.time())

        # We can't use set_signed_cookie() because we need to unsign the
        # query string using Signer() and for some reason the raw cookie
        # value fails to pass the sig check.
        signed = signer.sign(encoded)

        # Send to results page
        response = HttpResponseRedirect('../../results/')
        response.set_cookie('resultUrl', signed)
        response.delete_cookie('wizard_survey_wizard')
        return response

    def process_step(self, form):
        # By default, the big CSRF tokens get needlessly stored in the cookie
        # and take up a lot of space. This is bad because cookies have a
        # small limit.
        dict = self.get_form_step_data(form)
        return {
            key: val for key, val in dict.items() if (
                key != 'csrfmiddlewaretoken')}

    @staticmethod
    def build_views():
        # Create view wrappers for our assessments.
        wizard_views = {}
        for k, form_list in get_form_lists().items():
            wizard_views[k] = AssessmentWizard.as_view(
                form_list=form_list,
                url_name=f'assessment_{k}_step',
                template_name='teachers_digital_platform/assess-page.html',
            )
        return wizard_views


def _handle_result_url(request: HttpRequest, raw: str, code: str,
                       is_student: bool):
    res = urlEncode.loads(code)
    if res is None:
        return HttpResponseRedirect('../')

    rendered = render_to_string(
        'teachers_digital_platform/assess-results.html',
        {
            'is_student': is_student,
            'request': request,
            'r_param': raw,
            'assessment': res['assessment'],
            'subtotals': res['subtotals'],
            'time': time.gmtime(res['time']),
        },
    )
    return HttpResponse(status=200, content=rendered)


def student_results(request: HttpRequest):
    """
    Student results page
    """
    if request.method != 'GET':
        return HttpResponse(status=404)

    raw = request.COOKIES['resultUrl']
    if not isinstance(raw, str):
        return HttpResponseRedirect('../')

    try:
        result_url = signing.Signer().unsign(raw)
    except signing.BadSignature:
        return HttpResponseRedirect('../')

    return _handle_result_url(request, raw, result_url, True)


def show_results(request: HttpRequest):
    """
    Show results page
    """
    if request.method != 'GET':
        return HttpResponse(status=404)

    raw = request.GET['r']
    if not isinstance(raw, str):
        return HttpResponseRedirect('../')

    try:
        result_url = signing.Signer().unsign(raw)
    except signing.BadSignature:
        return HttpResponseRedirect('../')

    return _handle_result_url(request, raw, result_url, False)
