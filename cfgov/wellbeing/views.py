from django.shortcuts import render
from django.utils.translation import gettext_noop as _

from core.views import TranslatedTemplateView
from wellbeing.forms import FWBScore, ResultsForm


class ResultsView(TranslatedTemplateView):
    template_name = 'wellbeing/results.html'

    # for simplicity, answers below are reordered in order of worst to best
    QUESTIONS = [
        {
            # Question 1
            'question': _('I could handle a major unexpected expense'),
            'answers': [
                _('Not at all'),
                _('Very little'),
                _('Somewhat'),
                _('Very well'),
                _('Completely'),
            ]
        },
        {
            # Question 2
            'question': _('I am securing my financial future'),
            'answers': [
                _('Not at all'),
                _('Very little'),
                _('Somewhat'),
                _('Very well'),
                _('Completely'),
            ]
        },
        {
            # Question 3
            'question': _('Because of my money situation, I feel like I will '
                          'never have the things I want in life'),
            'answers': [
                _('Completely'),
                _('Very well'),
                _('Somewhat'),
                _('Very little'),
                _('Not at all'),
            ]
        },
        {
            # Question 4
            'question': _('I can enjoy life because of the way I\'m managing '
                          'my money'),
            'answers': [
                _('Not at all'),
                _('Very little'),
                _('Somewhat'),
                _('Very well'),
                _('Completely'),
            ]
        },
        {
            # Question 5
            'question': _('I am just getting by financially'),
            'answers': [
                _('Completely'),
                _('Very well'),
                _('Somewhat'),
                _('Very little'),
                _('Not at all'),
            ]
        },
        {
            # Question 6
            'question': _('I am concerned that the money I have or will save '
                          'won\'t last'),
            'answers': [
                _('Completely'),
                _('Very well'),
                _('Somewhat'),
                _('Very little'),
                _('Not at all'),
            ]
        },
        {
            # Question 7
            'question': _('Giving a gift for a wedding, birthday or other '
                          'occasion would put a strain on my finances for '
                          'the month'),
            'answers': [
                _('Always'),
                _('Often'),
                _('Sometimes'),
                _('Rarely'),
                _('Never'),
            ]
        },
        {
            # Question 8
            'question': _('I have money left over at the end of the month'),
            'answers': [
                _('Never'),
                _('Rarely'),
                _('Sometimes'),
                _('Often'),
                _('Always'),
            ]
        },
        {
            # Question 9
            'question': _('I am behind with my finances'),
            'answers': [
                _('Always'),
                _('Often'),
                _('Sometimes'),
                _('Rarely'),
                _('Never'),
            ]
        },
        {
            # Question 10
            'question': _('My finances control my life'),
            'answers': [
                _('Always'),
                _('Often'),
                _('Sometimes'),
                _('Rarely'),
                _('Never'),
            ]
        }
    ]

    SCORING = {
        'read-self': {
            _('18-61'): [
                14, 19, 22, 25, 27, 29, 31, 32, 34, 35, 37, 38, 40, 41, 42,
                44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62,
                63, 65, 66, 68, 69, 71, 73, 75, 78, 81, 86
            ],
            _('62-plus'): [
                14, 20, 24, 26, 29, 31, 33, 35, 36, 38, 39, 41, 42, 44, 45,
                46, 48, 49, 50, 52, 53, 54, 56, 57, 58, 60, 61, 63, 64, 66,
                67, 69, 71, 73, 75, 77, 79, 82, 84, 88, 95
            ]
        },
        'read-to-me': {
            _('18-61'): [
                16, 21, 24, 27, 29, 31, 33, 34, 36, 38, 39, 40, 42, 43, 44,
                45, 47, 48, 49, 50, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63,
                65, 66, 68, 70, 71, 73, 76, 78, 81, 85, 91
            ],
            _('62-plus'): [
                18, 23, 26, 28, 30, 32, 33, 35, 36, 38, 39, 40, 41, 43, 44,
                45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 60, 61,
                62, 64, 65, 67, 68, 70, 72, 75, 77, 81, 87
            ]
        }
    }

    avg_score = FWBScore.avg()

    group_means = {
        'age': [
            (_('18-24 year olds'), FWBScore(51)),
            (_('25-34 year olds'), FWBScore(51)),
            (_('35-44 year olds'), FWBScore(52)),
            (_('45-54 year olds'), FWBScore(54)),
            (_('55-64 year olds'), FWBScore(55)),
            (_('65-74 year olds'), FWBScore(61)),
            (_('75+ year olds'), FWBScore(60)),
        ],
        'income': [
            (_('Less than $20,000'), FWBScore(46)),
            (_('$20,000 to 29,999'), FWBScore(49)),
            (_('$30,000 to 49,999'), FWBScore(51)),
            (_('$50,000 to 74,999'), FWBScore(55)),
            (_('$75,000 to 99,999'), FWBScore(56)),
            (_('$100,000 and higher'), FWBScore(60)),
        ],
        'employment': [
            (_('Self-employed'), FWBScore(54)),
            (_('Full-time or part-time'), FWBScore(54)),
            (_('Homemaker'), FWBScore(54)),
            (_('Student'), FWBScore(51)),
            (_('Sick or disabled'), FWBScore(44)),
            (_('Unemployed or laid off'), FWBScore(45)),
            (_('Retired'), FWBScore(60)),
        ],
    }

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)

        context.update({
            'avg_score': FWBScore.avg(),
            'group_means': self.group_means,
        })

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form = ResultsForm(request.POST)

        if not form.is_valid():
            return render(request, 'wellbeing/error.html', context, status=400)

        context.update({
            'questions': self.QUESTIONS,
            'answers': form.cleaned_data['answers'],
            'user_score': form.cleaned_data['user_score'],
        })

        return self.render_to_response(context)
