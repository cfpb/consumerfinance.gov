from __future__ import division
from collections import OrderedDict

from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView


# def results(request):
#     if request is GET:
#         return render(template, questions)
#
#     request.POST
#     do some logic
#     add results to context
#
#     return render(template, questions + results)
#
#
# class ResultsView(TemplateView):
#     template_name = 'foo.html'
#
#     def get_context_data(self, ...):
#         context['questions'] = question
#         return context
#
#     def post(self):
#         do some logic
#         create a new context with questions and results
#         return render(template, questions + results)
#
# class FWBSurveyForm(forms.Form):
#     question1 = ...
#     question2 = ...
#
#     def clean(self):
#         self.results = ...
#
# def test_form_no_input
# def test_form_all_zeros
#     form = Form({'q1': 0, 'q2': 0...})
#     form.is_valid
#     self.assertEquals(form.cleaned_data['results'], whatever)
#
# class ResultsView(TemplateView):
#     def get_context_data(self, ):
#         context['form'] = form()
#
#     def post(self):
#         form = FWBSurveyForm(request.POST)
#         if form.is_valid:
#             form.results

class FWBScore(object):
    HIGH = 95
    LOW = 14
    AVG = 54

    def __init__(self, score):
        self.score = score

    def __str__(self):
        return str(self.score)

    @classmethod
    def avg(cls):
        return cls(cls.AVG)

    @property
    def pct(self):
        return ((self.score - self.LOW) / (self.HIGH - self.LOW)) * 100

    @property
    def color(self):
        if self.score < 40:
            return '#e05f21'
        elif self.score < 50:
            return '#f9921c'
        elif self.score < 60:
            return '#a6a329'
        elif self.score < 70:
            return '#44a839'
        else:  # score >= 70
            return '#398c7a'


class ResultsView(TemplateView):
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

        # process user data
        if len(request.POST) != 13:  # 10 Qs + 2 grouping Qs + CSRF token
            return render_to_response('wellbeing/error.html', context)

        answers = []
        answer_values = 0

        for i in range(1, 11):
            q = "question-%s" % i
            answers.append(int(request.POST[q]))
            answer_values += int(request.POST[q])

        method = request.POST['method']
        age = request.POST['age']
        user_score = FWBScore(self.SCORING[method][age][answer_values])

        # user_pct = user_score.pct
        # if user_pct > 50:
        #     user_pct_spectrum = 100 - user_pct
        #     score_box_positioning = 'right'
        # else:
        #     user_pct_spectrum = user_pct
        #     score_box_positioning = 'left'

        context.update({
            'questions': self.QUESTIONS,
            'answers': answers,
            'user_score': user_score,
        })

        return self.render_to_response(context)


def old_results(request):
    context = {}

    def get_score_pct(score, high, low):
        return ((score - low) / (high - low)) * 100

    def get_score_color(score):
        if score < 40:
            return '#e05f21'
        elif score < 50:
            return '#f9921c'
        elif score < 60:
            return '#a6a329'
        elif score < 70:
            return '#44a839'
        else:  # score >= 70
            return '#398c7a'

    # for simplicity, answers below are reordered in order of worst to best
    questions = [
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

    scoring = {
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

    low = 14
    high = 95
    avg_score = 54
    avg_color = get_score_color(avg_score)
    avg_pct = get_score_pct(avg_score, high, low)
    if avg_pct > 50:
        avg_pct_spectrum = 100 - avg_pct
    else:
        avg_pct_spectrum = avg_pct

    group_means = {
        'age': OrderedDict([
            ('18-24 year olds', {
                'mean': 51,
                'pct': get_score_pct(51, high, low),
                'color': get_score_color(51)
            }),
            ('25-34 year olds', {
                'mean': 51,
                'pct': get_score_pct(51, high, low),
                'color': get_score_color(51)
            }),
            ('35-44 year olds', {
                'mean': 52,
                'pct': get_score_pct(52, high, low),
                'color': get_score_color(52)
            }),
            ('45-54 year olds', {
                'mean': 54,
                'pct': get_score_pct(54, high, low),
                'color': get_score_color(54)
            }),
            ('55-64 year olds', {
                'mean': 55,
                'pct': get_score_pct(55, high, low),
                'color': get_score_color(55)
            }),
            ('65-74 year olds', {
                'mean': 61,
                'pct': get_score_pct(61, high, low),
                'color': get_score_color(61)
            }),
            ('75+ year olds', {
                'mean': 60,
                'pct': get_score_pct(60, high, low),
                'color': get_score_color(60)
            }),
        ]),
        'income': OrderedDict([
            ('Less than $20,000', {
                'mean': 46,
                'pct': get_score_pct(46, high, low),
                'color': get_score_color(46)
            }),
            ('$20,000 to 29,999', {
                'mean': 49,
                'pct': get_score_pct(49, high, low),
                'color': get_score_color(49)
            }),
            ('$30,000 to 49,999', {
                'mean': 51,
                'pct': get_score_pct(51, high, low),
                'color': get_score_color(51)
            }),
            ('$50,000 to 74,999', {
                'mean': 55,
                'pct': get_score_pct(55, high, low),
                'color': get_score_color(55)
            }),
            ('$75,000 to 99,999', {
                'mean': 56,
                'pct': get_score_pct(56, high, low),
                'color': get_score_color(56)
            }),
            ('$100,000 and higher', {
                'mean': 60,
                'pct': get_score_pct(60, high, low),
                'color': get_score_color(60)
            }),
        ]),
        'employment': OrderedDict([
            ('Self-employed', {
                'mean': 54,
                'pct': get_score_pct(54, high, low),
                'color': get_score_color(54)
            }),
            ('Full-time or part-time', {
                'mean': 54,
                'pct': get_score_pct(54, high, low),
                'color': get_score_color(54)
            }),
            ('Homemaker', {
                'mean': 54,
                'pct': get_score_pct(54, high, low),
                'color': get_score_color(54)
            }),
            ('Student', {
                'mean': 51,
                'pct': get_score_pct(51, high, low),
                'color': get_score_color(51)
            }),
            ('Sick or disabled', {
                'mean': 44,
                'pct': get_score_pct(44, high, low),
                'color': get_score_color(44)
            }),
            ('Unemployed or laid off', {
                'mean': 45,
                'pct': get_score_pct(45, high, low),
                'color': get_score_color(45)
            }),
            ('Retired', {
                'mean': 60,
                'pct': get_score_pct(60, high, low),
                'color': get_score_color(60)
            }),
        ]),
    }

    if request.method == 'POST':
        if len(request.POST) != 13:  # 10 Qs + 2 grouping Qs + CSRF token
            return render_to_response('wellbeing/error.html', context)

        answers = []
        answer_values = 0

        for i in range(1, 11):
            q = "question-%s" % i
            answers.append(int(request.POST[q]))
            answer_values += int(request.POST[q])

        method = request.POST['method']
        age = request.POST['age']
        user_score = scoring[method][age][answer_values]
        user_color = get_score_color(user_score)

        user_pct = get_score_pct(user_score, high, low)
        if user_pct > 50:
            user_pct_spectrum = 100 - user_pct
            score_box_positioning = 'right'
        else:
            user_pct_spectrum = user_pct
            score_box_positioning = 'left'

        context['questions'] = questions
        context['answers'] = answers
        context['avg_score'] = avg_score
        context['avg_color'] = avg_color
        context['avg_pct'] = avg_pct
        context['avg_pct_spectrum'] = avg_pct_spectrum
        context['group_means'] = group_means
        context['user_score'] = user_score
        context['user_color'] = user_color
        context['user_pct'] = user_pct
        context['user_pct_spectrum'] = user_pct_spectrum
        context['score_box_positioning'] = score_box_positioning
    else:
        # Handle a direct request of the page with no POSTed questionnaire
        return redirect('../')

    return render_to_response('wellbeing/results.html', context)
