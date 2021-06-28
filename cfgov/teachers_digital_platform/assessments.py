from typing import Dict, List, Tuple, Any

from django import forms
from os.path import dirname

from .TemplateField import TemplateField
from .forms import AssessmentForm, markup

import csv
import hashlib
import json


def _question_row(row: Dict[str, str]):
    return {
        'q': row['Question'],
        's': row['Section'],
        'p': row['Page'],
        'a': row['Answer type'],
        'w': row['Answer worth'],
    }


def _answer_types_row(row: Dict[str, str]):
    return {
        'k': row['Key'],
        'c': row['Choices'],
    }


class ChoiceList:
    """
    To save mem, we'll only need a couple of these objects in practice
    """

    def __init__(self, labels: List[str]):
        self.labels = labels
        self.choices = tuple(
            (str(k), v) for k, v in enumerate(labels)
        )

    @staticmethod
    def from_string(s: str):
        labels = list(x.strip() for x in s.split('|'))
        return ChoiceList(labels)


choice_lists: Dict[str, ChoiceList] = {}


class Question:
    """
    Base question
    """

    def __init__(self, num: int, section: str):
        self.key = f'q{num}'
        self.num = num
        self.section = section

    def get_score(self):
        return 0

    def get_field(self):
        return None


class ChoiceQuestion(Question):
    """
    Choice question
    """

    def __init__(self, num: int, section: str, label: str,
                 choice_list: ChoiceList, answer_values: List[float]):
        super().__init__(num, section)
        self.choice_list = choice_list
        self.label = label
        self.answer_values = answer_values

    def get_choices(self) -> Tuple[Tuple[str, str], ...]:
        return self.choice_list.choices

    def get_score(self, answer) -> float:
        answer = int(answer)
        assert answer >= 0
        assert answer < len(self.choice_list.labels)
        return self.answer_values[answer]

    def get_field(self):
        label = ''.join([
            markup('<strong class="question-num">'),
            str(self.num),
            '.',
            markup('</strong>'),
            ' ',
            self.label,
        ])
        return {
            'key': self.key,
            'field': forms.ChoiceField(
                widget=forms.RadioSelect({
                    'class': 'ChoiceField'
                }),
                choices=self.choice_list.choices,
                label=label,
                required=True,
            ),
        }


class AssessmentPage:
    """
    Page of an assessment
    """

    def __init__(self, heading: str, questions: List[Question]):
        self.heading = heading
        self.questions = questions

    def get_fields(self, prefix_tpls: Dict[str, str]):
        fields = {}

        for question in self.questions:
            if question.key in prefix_tpls:
                fields[f'before_{question.key}'] = TemplateField(
                    prefix_tpls[question.key])

            obj = question.get_field()
            fields[obj['key']] = obj['field']

        return fields

    def get_score(self, all_cleaned_data):
        total = 0
        question_scores = {}

        for question in self.questions:
            answer = all_cleaned_data[question.key]
            score = question.get_score(answer)
            total += score
            question_scores[question] = score

        return {
            'total': total,
            'question_scores': question_scores,
        }

    def get_form_class(self, name: str, inserted_key_field: str,
                       prefix_tpls: Dict[str, str]):
        fields = self.get_fields(prefix_tpls)

        # Put a hidden "_k" field in the form to tell the Assessment
        # wizard can figure out what assessment it's working with
        # We pull this from initial data so there's no way the client
        # can edit this.
        if inserted_key_field != '':
            fields['_k'] = forms.CharField(
                widget=forms.HiddenInput,
                initial=inserted_key_field,
                disabled=True,
            )

        return type(
            name,
            (AssessmentForm,),
            fields,
        )


class Assessment:
    """
    A full assessment
    """

    def __init__(self, key: str, meta: Dict[str, Any],
                 pages: List[AssessmentPage]):
        self.key = key
        self.meta = meta
        self.pages = pages

    def get_score(self, all_cleaned_data) -> float:
        total = 0
        question_scores = {}
        page_scores = {}

        for page in self.pages:
            score = page.get_score(all_cleaned_data)
            subtotal = score['total']
            page_scores[page] = subtotal
            question_scores.update(score['question_scores'])
            total += subtotal

        return {
            'question_scores': question_scores,
            'page_scores': page_scores,
            'total': total,
        }

    def get_form_list(self, assessment_key: str):
        page_classes = []

        for page_i, page in enumerate(self.pages):
            name = str(page_i + 1)
            inserted_key_field = self.key if page_i == 0 else ''

            # Unique class name for each assessment + page (not technically
            # required but feels safer)
            hash = hashlib.md5((assessment_key + '|' + name).encode())
            classname = 'FormPage' + hash.hexdigest()

            page_classes.append((name, page.get_form_class(
                classname, inserted_key_field, self.meta['prefix_tpls'])))

        return tuple(page_classes)

    @staticmethod
    def setup_choices():
        if len(choice_lists) > 0:
            return
        path = f'{dirname(__file__)}/assessment-data/answer-types.csv'
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_answer_types_row(row) for row in reader):
                choice_lists[row['k']] = ChoiceList.from_string(row['c'])

    @staticmethod
    def factory(key: str):
        """Build an assessment from CSV"""
        assert key in available_assessments

        Assessment.setup_choices()

        q = 1
        last_page = None
        pages: List[AssessmentPage] = []
        questions: List[Question] = []

        def end_page(last_page: str):
            page = AssessmentPage(f'Page {last_page}', questions.copy())
            pages.append(page)
            questions.clear()

        path = f'{dirname(__file__)}/assessment-data/{key}.csv'
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_question_row(row) for row in reader):
                if last_page is None:
                    last_page = row['p']
                if row['p'] != last_page:
                    end_page(last_page)

                last_page = row['p']

                values = list(int(x.strip()) for x in row['w'].split(' '))
                question = ChoiceQuestion(
                    q, row['s'], row['q'], choice_lists[row['a']], values)
                questions.append(question)
                q += 1
        end_page(last_page)

        path = f'{dirname(__file__)}/assessment-data/{key}-meta.json'
        with open(path) as json_file:
            meta = json.load(json_file)

        return Assessment(key, meta, pages)


available_assessments = ('9-12')


def get_assessment(key) -> Assessment:
    assert key in available_assessments
    return Assessment.factory('9-12')


def get_all_assessments() -> Dict[str, Assessment]:
    return {
        '9-12': get_assessment('9-12')
    }


def get_form_lists():
    form_lists = {}
    for k, assessment in get_all_assessments().items():
        form_lists[k] = assessment.get_form_list(k)
    return form_lists
