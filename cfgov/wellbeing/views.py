from collections import OrderedDict

from django.shortcuts import render

from core.views import TranslatedTemplateView
from wellbeing.forms import FWBScore, ResultsForm


class ResultsView(TranslatedTemplateView):
    template_name = 'wellbeing/results.html'

    # for simplicity, answers below are reordered in order of worst to best
    QUESTIONS = [
        {
            # Question 1
            'question': 'I could handle a major unexpected expense',
            'answers': [
                'Not at all',
                'Very little',
                'Somewhat',
                'Very well',
                'Completely',
            ]
        },
        {
            # Question 2
            'question': 'I am securing my financial future',
            'answers': [
                'Not at all',
                'Very little',
                'Somewhat',
                'Very well',
                'Completely',
            ]
        },
        {
            # Question 3
            'question': 'Because of my money situation, I feel like I will '
                        'never have the things I want in life',
            'answers': [
                'Completely',
                'Very well',
                'Somewhat',
                'Very little',
                'Not at all',
            ]
        },
        {
            # Question 4
            'question': 'I can enjoy life because of the way I\'m managing my '
                        'money',
            'answers': [
                'Not at all',
                'Very little',
                'Somewhat',
                'Very well',
                'Completely',
            ]
        },
        {
            # Question 5
            'question': 'I am just getting by financially',
            'answers': [
                'Completely',
                'Very well',
                'Somewhat',
                'Very little',
                'Not at all',
            ]
        },
        {
            # Question 6
            'question': 'I am concerned that the money I have or will save '
                        'won\'t last',
            'answers': [
                'Completely',
                'Very well',
                'Somewhat',
                'Very little',
                'Not at all',
            ]
        },
        {
            # Question 7
            'question': 'Giving a gift for a wedding, birthday or other '
                        'occasion would put a strain on my finances for the '
                        'month',
            'answers': [
                'Always',
                'Often',
                'Sometimes',
                'Rarely',
                'Never',
            ]
        },
        {
            # Question 8
            'question': 'I have money left over at the end of the month',
            'answers': [
                'Never',
                'Rarely',
                'Sometimes',
                'Often',
                'Always',
            ]
        },
        {
            # Question 9
            'question': 'I am behind with my finances',
            'answers': [
                'Always',
                'Often',
                'Sometimes',
                'Rarely',
                'Never',
            ]
        },
        {
            # Question 10
            'question': 'My finances control my life',
            'answers': [
                'Always',
                'Often',
                'Sometimes',
                'Rarely',
                'Never',
            ]
        }
    ]

    SCORING = {
        'read-self': {
            '18-61': [
                14, 19, 22, 25, 27, 29, 31, 32, 34, 35, 37, 38, 40, 41, 42,
                44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62,
                63, 65, 66, 68, 69, 71, 73, 75, 78, 81, 86
            ],
            '62-plus': [
                14, 20, 24, 26, 29, 31, 33, 35, 36, 38, 39, 41, 42, 44, 45,
                46, 48, 49, 50, 52, 53, 54, 56, 57, 58, 60, 61, 63, 64, 66,
                67, 69, 71, 73, 75, 77, 79, 82, 84, 88, 95
            ]
        },
        'read-to-me': {
            '18-61': [
                16, 21, 24, 27, 29, 31, 33, 34, 36, 38, 39, 40, 42, 43, 44,
                45, 47, 48, 49, 50, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63,
                65, 66, 68, 70, 71, 73, 76, 78, 81, 85, 91
            ],
            '62-plus': [
                18, 23, 26, 28, 30, 32, 33, 35, 36, 38, 39, 40, 41, 43, 44,
                45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 60, 61,
                62, 64, 65, 67, 68, 70, 72, 75, 77, 81, 87
            ]
        }
    }

    avg_score = FWBScore.avg()

    group_means = {
        'age': OrderedDict([
            ('18-24 year olds', FWBScore(51)),
            ('25-34 year olds', FWBScore(51)),
            ('35-44 year olds', FWBScore(52)),
            ('45-54 year olds', FWBScore(54)),
            ('55-64 year olds', FWBScore(55)),
            ('65-74 year olds', FWBScore(61)),
            ('75+ year olds', FWBScore(60)),
        ]),
        'income': OrderedDict([
            ('Less than $20,000', FWBScore(46)),
            ('$20,000 to 29,999', FWBScore(49)),
            ('$30,000 to 49,999', FWBScore(51)),
            ('$50,000 to 74,999', FWBScore(55)),
            ('$75,000 to 99,999', FWBScore(56)),
            ('$100,000 and higher', FWBScore(60)),
        ]),
        'employment': OrderedDict([
            ('Self-employed', FWBScore(54)),
            ('Full-time or part-time', FWBScore(54)),
            ('Homemaker', FWBScore(54)),
            ('Student', FWBScore(51)),
            ('Sick or disabled', FWBScore(44)),
            ('Unemployed or laid off', FWBScore(45)),
            ('Retired', FWBScore(60)),
        ]),
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
