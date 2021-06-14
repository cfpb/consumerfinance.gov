import time

from django.http.response import HttpResponseRedirect
from formtools.wizard.views import NamedUrlCookieWizardView

from .assessments import available_assessments, get_assessment
from . import urlEncode


class AssessmentWizard(NamedUrlCookieWizardView):
    def done(self, form_list, **kwargs):
        # Find assessment based on hidden "_k" question in page1
        first_page = self.get_form('page1')
        assessment_key = first_page.fields['_k'].initial
        if not isinstance(assessment_key, str) or not assessment_key in available_assessments:
            # Hmm this isn't right
            response = HttpResponseRedirect('../')
            response.delete_cookie('resultUrl')
            response.delete_cookie('wizard_survey_wizard')
            return response

        assessment = get_assessment(assessment_key)

        # Calc score and encode in URL
        score = assessment.get_score(self.get_all_cleaned_data())
        encoded = urlEncode.dumps(assessment, score['subtotals'], time.time())

        # Send to results page
        response = HttpResponseRedirect('../results/')
        response.set_signed_cookie('resultUrl', encoded)
        response.delete_cookie('wizard_survey_wizard')
        return response

    def process_step(self, form):
        # By default, the big CSRF tokens get needlessly stored in the cookie and
        # take up a lot of space. This is bad because cookies have a small limit.
        dict = self.get_form_step_data(form)
        return {key: val for key, val in dict.items() if key != 'csrfmiddlewaretoken'}
