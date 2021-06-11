from django.http.response import HttpResponseRedirect
from formtools.wizard.views import NamedUrlCookieWizardView

from teachers_digital_platform.forms import get_pages


surveys_dict = {}
surveys_dict['gr3'] = get_pages('gr3')['question_dict']

class SurveyWizard(NamedUrlCookieWizardView):
    def done(self, form_list, **kwargs):
        first_page = self.get_form('page1')
        survey_key = first_page.fields['_sk'].initial
        
        data = self.get_all_cleaned_data()
        total = 0
        answers = []

        for key, question in surveys_dict[survey_key].items():
            answer = int(data[key])
            answers.append(str(answer))
            total += question.scores[answer]

        encoded = ''.join(answers) + ':' + str(total)
        
        response = HttpResponseRedirect('../results/')
        response.set_signed_cookie('resultUrl', encoded)
        return response

    def process_step(self, form):
        # By default, the big CSRF tokens get needlessly stored in the cookie and
        # take up a lot of space. This is bad because cookies have a small limit.
        dict = self.get_form_step_data(form)
        return {key:val for key, val in dict.items() if key != 'csrfmiddlewaretoken'}
