import re
import time
from typing import Dict

from django.core import signing
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.template.loader import render_to_string

from formtools.wizard.views import NamedUrlCookieWizardView

from . import urlEncode
from .assessments import AVAILABLE_ASSESSMENTS, Question, get_assessment
from .resultsContent import ResultsContent


signer = signing.Signer()
tdp = 'teachers_digital_platform'


class AssessmentWizard(NamedUrlCookieWizardView):
    assessment_key = ''

    def done(self, form_list, **kwargs):
        assessment = get_assessment(self.assessment_key)

        # Calc score and encode in URL
        question_scores: Dict[Question, float] = assessment.get_score(
            self.get_all_cleaned_data())['question_scores']
        part_scores: Dict[str, float] = {}

        for question, score in question_scores.items():
            if question.part not in part_scores:
                part_scores[question.part] = 0
            part_scores[question.part] += score

        subtotals = list(v for k, v in sorted(part_scores.items()))
        encoded = urlEncode.dumps(assessment, subtotals, int(time.time()))

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
        dict = self.get_form_step_data(form).copy()
        del dict['csrfmiddlewaretoken']
        return dict

    def render(self, form=None, **kwargs):
        # Overriding so we can inject useful data
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)

        # Push the assessment and active page into template
        page_idx = int(re.sub(r'\D+', '', context['step'])) - 1
        assessment = get_assessment(self.assessment_key)
        context['assessment'] = assessment
        context['page_idx'] = page_idx
        context['questions_by_page'] = assessment.num_questions_by_page()

        return self.render_to_response(context)

    @staticmethod
    def build_views():
        # Create view wrappers for our assessments.
        wizard_views = {}
        for key in AVAILABLE_ASSESSMENTS:
            wizard_views[key] = AssessmentWizard.as_view(
                assessment_key=key,
                form_list=get_assessment(key).get_form_list(),
                url_name=f'assessment_{key}_step',
                template_name=f'{tdp}/assess/form-page.html',
            )
        return wizard_views


def _handle_result_url(request: HttpRequest, raw: str, code: str,
                       is_student: bool):
    res = urlEncode.loads(code)
    if res is None:
        return HttpResponseRedirect('../')

    total = sum(res['subtotals'])
    adjusted = total * res['assessment'].get_score_multiplier()
    student_view = False if 'share_view' in request.GET else is_student

    rendered = render_to_string(
        f'{tdp}/assess/results-{res["key"]}.html',
        {
            'content': ResultsContent.factory(res['key']),
            'is_student': student_view,
            'request': request,
            'r_param': raw,
            'assessment': res['assessment'],
            'subtotals': res['subtotals'],
            'score': adjusted,
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

    if 'resultUrl' not in request.COOKIES:
        return HttpResponseRedirect('../')

    raw = request.COOKIES['resultUrl']
    try:
        result_url = signer.unsign(raw)
    except signing.BadSignature:
        return HttpResponseRedirect('../')

    return _handle_result_url(request, raw, result_url, True)


def view_results(request: HttpRequest):
    """
    View results page
    """
    if request.method != 'GET':
        return HttpResponse(status=404)

    raw = request.GET['r']
    if not isinstance(raw, str):
        return HttpResponseRedirect('../')

    try:
        result_url = signer.unsign(raw)
    except signing.BadSignature:
        return HttpResponseRedirect('../')

    return _handle_result_url(request, raw, result_url, False)


def _grade_level_page(request: HttpRequest, key: str):
    assessment = get_assessment(key)
    rendered = render_to_string(
        f'{tdp}/assess/grade-level-{key}.html',
        {
            'request': request,
            'assessment': assessment,
        },
    )
    return HttpResponse(status=200, content=rendered)


def create_grade_level_page_handler(key: str):
    # Critically this captures the key in the closure for later invocation.
    return lambda request: _grade_level_page(request, key)
