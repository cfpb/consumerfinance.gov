import json
import logging

import requests
from django.conf import settings
from django.contrib import messages
from django.http import (Http404, HttpResponse, HttpResponseForbidden,
                         JsonResponse)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from govdelivery.api import GovDelivery
from requests_toolbelt.multipart.encoder import MultipartEncoder

from core.forms import ExternalURLForm
from core.utils import extract_answers_from_request

logger = logging.getLogger(__name__)

REQUIRED_PARAMS_GOVDELIVERY = ['email', 'code']


@csrf_exempt
@require_http_methods(['POST'])
def govdelivery_subscribe(request):
    """
    View that checks to see if the request is AJAX, attempts to subscribe
    the user, then either redirects to an error/success page (non-AJAX) or
    in the case of AJAX, returns some JSON to tell the front-end.
    """
    is_ajax = request.is_ajax()
    if is_ajax:
        passing_response = JsonResponse({'result': 'pass'})
        failing_response = JsonResponse({'result': 'fail'})
    else:
        passing_response = redirect('govdelivery:success')
        failing_response = redirect('govdelivery:server_error')
    for required_param in REQUIRED_PARAMS_GOVDELIVERY:
        if (required_param not in request.POST or
                not request.POST.get(required_param)):
            return failing_response if is_ajax else \
                redirect('govdelivery:user_error')
    email_address = request.POST['email']
    codes = request.POST.getlist('code')
    gd = GovDelivery(account_code=settings.ACCOUNT_CODE)
    try:
        subscription_response = gd.set_subscriber_topics(email_address, codes)
        if subscription_response.status_code != 200:
            return failing_response
    except Exception:
        return failing_response
    answers = extract_answers_from_request(request)
    for question_id, answer_text in answers:
        gd.set_subscriber_answers_to_question(email_address,
                                              question_id,
                                              answer_text)
    return passing_response


REQUIRED_PARAMS_REGSGOV = [
    'general_comment',
]


@csrf_exempt
@require_http_methods(['POST'])
def regsgov_comment(request):
    """
    View that checks to see if the request is AJAX, attempts to submit
    the comment, then either redirects to an error/success page (non-AJAX) or
    in the case of AJAX, returns some JSON to tell the front-end.
    """
    is_ajax = request.is_ajax()
    if is_ajax:
        failing_response = JsonResponse({'result': 'fail'})
    else:
        failing_response = redirect('reg_comment:server_error')

    for required_param in REQUIRED_PARAMS_REGSGOV:
        if not request.POST.get(required_param):
            return failing_response if is_ajax \
                else redirect('reg_comment:user_error')

    try:
        submission_response = submit_comment(request.POST)
        if submission_response.status_code != 201:
            return failing_response
    except Exception:
        return failing_response

    json_data = json.loads(submission_response.text)
    tracking_number = json_data.get('trackingNumber')

    # For non-ajax, tracking number will appear as a message with tag: success
    messages.success(request, tracking_number)

    return JsonResponse(
        {'result': 'pass', 'tracking_number': tracking_number}
    ) if is_ajax else redirect('reg_comment:success')


def submit_comment(data):
    """
    View that actually performs the comment submission via the Regulations.gov
    Comment API, then returns the response.
    """

    url_to_call = "{}?api_key={}&D={}".format(settings.REGSGOV_BASE_URL,
                                              settings.REGSGOV_API_KEY,
                                              data['comment_on'])

    parsed_data = MultipartEncoder(
        fields={
            'first_name': (data['first_name'] if data.get('first_name')
                           else u'Anonymous'),
            'last_name': (data['last_name'] if data.get('last_name')
                          else u'Anonymous'),
            'email': (data['email'] if data.get('email') else u'NA'),
            'general_comment': data['general_comment'],
            'comment_on': data['comment_on'],
            'organization': u'NA'
        }
    )

    response = requests.post(url_to_call, data=parsed_data,
                             headers={
                                 'Content-Type': parsed_data.content_type
                             })

    return response


@csrf_exempt
def csp_violation_report(request):
    if request.method == 'POST':
        try:
            csp_dict = json.loads(request.body)['csp-report']
        # bare except is non-ideal, but if parsing fails for any reason
        # we need to abort
        except:
            return HttpResponseForbidden()

        message_template = ('{blocked-uri} blocked on {document-uri}, '
                            'violated {violated-directive}')
        message = message_template.format(**csp_dict)
        logger.warn(message)
        return HttpResponse()
    return HttpResponseForbidden()


class ExternalURLNoticeView(FormMixin, TemplateView):
    template_name = 'external-site/index.html'
    form_class = ExternalURLForm

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ExternalURLNoticeView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ExternalURLNoticeView, self).get_form_kwargs()

        if self.request.method == 'GET':
            kwargs['data'] = self.request.GET

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ExternalURLNoticeView, self).get_context_data(**kwargs)

        form = self.get_form()
        context['form'] = form

        return context

    def get(self, request):
        form = self.get_form()
        if form.is_valid():
            return super(ExternalURLNoticeView, self).get(request)
        else:
            raise Http404("URL invalid, not whitelisted, or signature"
                          " validation failed")

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return redirect(form.cleaned_data['validated_url'])
