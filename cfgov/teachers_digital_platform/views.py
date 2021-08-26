import re
import time
from typing import Dict

from django.core import signing
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie

from formtools.wizard.views import NamedUrlCookieWizardView

from .resultsContent import ResultsContent
from .surveys import AVAILABLE_SURVEYS, ChoiceList, Question, get_survey
from .UrlEncoder import UrlEncoder


_tdp = 'teachers_digital_platform'
_signer = signing.Signer()


class SurveyWizard(NamedUrlCookieWizardView):
    """
    High level component representing the full multi-page form.
    """
    survey_key = ''

    def done(self, form_list, **kwargs):
        """
        Called after submitting the last page IF every subform is validated
        """
        survey = get_survey(self.survey_key)

        # Calc score and encode in URL
        question_scores: Dict[Question, float] = survey.get_score(
            self.get_all_cleaned_data())['question_scores']
        part_scores: Dict[str, float] = {}

        for question, score in question_scores.items():
            if question.part not in part_scores:
                part_scores[question.part] = 0
            part_scores[question.part] += score

        subtotals = list(v for k, v in sorted(part_scores.items()))

        url_encoder = UrlEncoder(AVAILABLE_SURVEYS)
        encoded = url_encoder.dumps(survey.key, subtotals, int(time.time()))

        # We can't use set_signed_cookie() because we need to unsign the
        # query string using Signer() and for some reason the raw cookie
        # value fails to pass the sig check.
        signed = _signer.sign(encoded)

        # Send to results page (current URL is survey/6-8/done/ )
        response = HttpResponseRedirect('../results/')
        response.set_cookie('resultUrl', signed)
        response.delete_cookie('wizard_survey_wizard')
        return response

    def process_step(self, form):
        """
        Process the page-specific data stored in the cookie

        By default, the big CSRF tokens get needlessly stored in the cookie
        and take up a lot of space. This is bad because cookies have a small
        limit.
        """
        data = self.get_form_step_data(form).copy()
        del data['csrfmiddlewaretoken']
        return data

    def render(self, form=None, **kwargs):
        """
        Called to render the form (and sneak some info into the template)
        """
        # Overriding so we can inject useful data
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)

        # Push the survey and active page into template
        page_idx = int(re.sub(r'\D+', '', context['step'])) - 1
        survey = get_survey(self.survey_key)
        context['survey'] = survey
        context['page_idx'] = page_idx
        context['questions_by_page'] = survey.num_questions_by_page()

        return self.render_to_response(context)

    @method_decorator(never_cache)
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @classmethod
    def build_views(cls):
        """
        For each survey key, a view object is returned that can handle a
        request for a single page.
        """
        wizard_views = {}
        choice_lists = ChoiceList.get_all()
        for key in AVAILABLE_SURVEYS:
            wizard_views[key] = cls.as_view(
                survey_key=key,
                form_list=get_survey(key, choice_lists).get_form_list(),
                # Note it's important this is kept in sync with the name
                # parameter in urls.py
                url_name=f'survey_{key}_step',
                template_name=f'{_tdp}/survey/form-page.html',
            )
        return wizard_views


def _handle_result_url(request: HttpRequest, raw: str, code: str,
                       is_student: bool):
    url_encoder = UrlEncoder(AVAILABLE_SURVEYS)
    res = url_encoder.loads(code)
    if res is None:
        return HttpResponseRedirect('../../../assess/survey/')

    survey = get_survey(res['key'])
    total = sum(res['subtotals'])
    adjusted = survey.adjust_total_score(total)
    student_view = False if 'share_view' in request.GET else is_student

    rendered = render_to_string(
        f'{_tdp}/survey/results-{res["key"]}.html',
        {
            'content': ResultsContent.factory(res['key']),
            'is_student': student_view,
            'request': request,
            'r_param': raw,
            'survey': survey,
            'subtotals': res['subtotals'],
            'score': adjusted,
            'time': time.gmtime(res['time']),
        },
    )
    return HttpResponse(status=200, content=rendered)


@never_cache
@vary_on_cookie
def student_results(request: HttpRequest):
    """
    Request handler for the student results page
    """
    if request.method != 'GET':
        return HttpResponse(status=404)

    if 'resultUrl' not in request.COOKIES:
        return HttpResponseRedirect('../../../assess/survey/')

    raw = request.COOKIES['resultUrl']
    try:
        result_url = _signer.unsign(raw)
    except signing.BadSignature:
        return HttpResponseRedirect('../../../assess/survey/')

    return _handle_result_url(request, raw, result_url, True)


@never_cache
@vary_on_cookie
def view_results(request: HttpRequest):
    """
    Request handler for the view results page
    """
    if request.method != 'GET':
        return HttpResponse(status=404)

    raw = request.GET['r']
    if not isinstance(raw, str):
        return HttpResponseRedirect('../../../assess/survey/')

    try:
        result_url = _signer.unsign(raw)
    except signing.BadSignature:
        return HttpResponseRedirect('../../../assess/survey/')

    return _handle_result_url(request, raw, result_url, False)


@never_cache
def _grade_level_page(request: HttpRequest, key: str):
    survey = get_survey(key)
    rendered = render_to_string(
        f'{_tdp}/survey/grade-level-{key}.html',
        {
            'request': request,
            'survey': survey,
        },
    )
    return HttpResponse(status=200, content=rendered)


def create_grade_level_page_handler(key: str):
    """
    Create a view handler for a particular grade-level intro page

    This makes sure the key is captured in the closure so it's correct
    when the lambda is executed.
    """
    return lambda request: _grade_level_page(request, key)
