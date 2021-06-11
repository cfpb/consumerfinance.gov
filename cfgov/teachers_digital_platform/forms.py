from django import forms
from django.forms.widgets import Widget


class Question:
    def __init__(self, type, label, scores):
        self.type = type
        self.label = label
        self.scores = scores


def get_data():
    return [
        [
            "Who is your hero?",
            "If you could live anywhere, where would it be?",
        ],
        [
            "What is your favorite family vacation?",
            "What really makes you angry?",
        ],
    ]

CHOICES = (
    ("0", "Zero"),
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
)

def createPageForm(fields, survey_key, name):
    if (name == 'page1'):
        fields['_sk'] = forms.CharField(
            widget=forms.HiddenInput,
            initial=survey_key,
            required=False,
            disabled=True,
        )

    return type(
        "SurveyPageForm",
        (forms.Form,), 
        fields,
    )

def get_pages(survey_key):
    data = get_data()
    pages = []
    named_classes = []
    question_dict = {}
    q_counter = 0

    for page_i, labels in enumerate(data):
        name = 'page' + str(page_i + 1)
        questions = []
        fields = {}

        for label in labels:
            key = 'q' + str(q_counter)
            q_counter = q_counter + 1
            
            question = Question(1, label, [0, 1, 2, 3, 4])
            question_dict[key] = question

            questions.append({
                'question': Question(1, label, [0, 1, 2, 3, 4]),
                'key': key,
            })

            fields[key] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=CHOICES,
                label=label,
            )

        pages.append({
            'name': name,
            'questions': questions,
        })
        named_class = ( name, createPageForm(fields, survey_key, name) )
        named_classes.append(named_class)
    
    return {
        'form_list': tuple(named_classes),
        'pages': pages,
        'question_dict': question_dict,
    }
