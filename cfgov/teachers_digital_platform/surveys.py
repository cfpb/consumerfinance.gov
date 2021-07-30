import csv
import hashlib
import json
from os.path import dirname
from typing import Any, Dict, List, Optional, Tuple

from django import forms

from .ChoiceWidget import ChoiceWidget
from .forms import SurveyForm, markup
from .TemplateField import TemplateField


PREFILL_ANSWERS = False

AVAILABLE_SURVEYS = ('3-5', '6-8', '9-12')


def _question_row(row: Dict[str, str]):
    return {
        'q': row['Question'],
        'pt': row['Part'],
        'pg': row['Page'],
        'a': row['Answer type'],
        'w': row['Answer worth'],
        's': row['Section'],
    }


def _answer_types_row(row: Dict[str, str]):
    return {
        'k': row['Key'],
        'c': row['Choices'],
    }


class ChoiceList:
    """
    To save mem, we'll only need a few of these objects in practice
    """

    def __init__(self, labels: List[str]):
        self.labels = labels
        self.choices = tuple(
            (str(k), v) for k, v in enumerate(labels)
        )

    @classmethod
    def from_string(cls, s: str):
        labels = list(x.strip() for x in s.split('|'))
        return cls(labels)

    @classmethod
    def get_all(cls):
        ret: Dict[str, cls] = {}

        path = f'{dirname(__file__)}/survey-data/answer-types.csv'
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_answer_types_row(row) for row in reader):
                ret[row['k']] = cls.from_string(row['c'])

        return ret


class Question:
    """
    Base question
    """

    def __init__(self, num: int, part: str):
        self.key = f'q{num}'
        self.num = num
        self.part = part

    def get_score(self, answer):
        return 0

    def get_field(self):
        return None


class ChoiceQuestion(Question):
    """
    Choice question
    """

    def __init__(self, num: int, part: str, label: str,
                 choice_list: ChoiceList, answer_values: List[float],
                 opts_list: Optional[ChoiceList] = None,
                 meta: Optional[Dict] = None):
        super().__init__(num, part)
        self.meta = {} if meta is None else meta
        self.choice_list = choice_list
        self.opts_list = opts_list
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

        initial = None
        if PREFILL_ANSWERS:
            initial = self.answer_values.index(max(self.answer_values))

        classes = ['ChoiceField', 'tdp-survey__choice-question']
        if 'atype' in self.meta:
            atype = self.meta["atype"]
            classes.append(f'tdp-survey__atype-{atype}')

        return {
            'key': self.key,
            'field': forms.ChoiceField(
                widget=ChoiceWidget(
                    {'class': ' '.join(classes)},
                    opts_list=self.opts_list
                ),
                choices=self.choice_list.choices,
                label=label,
                required=True,
                initial=initial,
            ),
        }


class SurveyPage:
    """
    Page of an survey
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

    def get_form_class(self, name: str, prefix_tpls: Dict[str, str]):
        return type(
            name,
            (SurveyForm,),
            self.get_fields(prefix_tpls),
        )


class Survey:
    """
    A full survey
    """

    def __init__(self, key: str, meta: Dict[str, Any],
                 pages: List[SurveyPage]):
        self.key = key
        self.meta = meta
        self.pages = pages

    def num_questions_by_page(self) -> List[int]:
        return list(len(page.questions) for page in self.pages)

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

    def adjust_total_score(self, total) -> float:
        if 'score_multiplier' not in self.meta:
            return total

        expr = self.meta['score_multiplier']

        if isinstance(expr, (float, int)):
            return total * expr

        if type(expr) is list and len(expr) == 3 and expr[1] == '/':
            return total * expr[0] / expr[2]

        raise ValueError(f'score_multiplier {expr} is unsupported')

    def get_form_list(self):
        page_classes = []

        for page_i, page in enumerate(self.pages):
            name = f'p{page_i + 1}'

            # Unique class name for each survey + page (not technically
            # required but feels safer)
            hash = hashlib.md5((self.key + '|' + name).encode())
            classname = 'FormPage' + hash.hexdigest()

            page_classes.append((name, page.get_form_class(
                classname, self.meta['prefix_tpls'])))

        return tuple(page_classes)

    @classmethod
    def factory(cls, key: str, choice_lists: Optional[Dict] = None):
        """Build an survey from CSV"""
        assert key in AVAILABLE_SURVEYS

        if choice_lists is None:
            choice_lists = ChoiceList.get_all()

        q = 1
        last_page = None
        pages: List[SurveyPage] = []
        questions: List[Question] = []

        def end_page(last_page: str):
            page = SurveyPage(f'Page {last_page}', questions.copy())
            pages.append(page)
            questions.clear()

        path = f'{dirname(__file__)}/survey-data/{key}.csv'
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_question_row(row) for row in reader):
                if last_page is None:
                    last_page = row['pg']
                if row['pg'] != last_page:
                    end_page(last_page)

                last_page = row['pg']

                values = list(int(x.strip()) for x in row['w'].split(' '))

                choices_key = row['a']
                if choices_key not in choice_lists:
                    msg = f'Unknown answer type {choices_key}'
                    raise NameError(msg)

                opts_key = f'{choices_key}-opts'
                opts_list = None
                if opts_key in choice_lists:
                    opts_list = choice_lists[opts_key].labels

                question = ChoiceQuestion(
                    q, row['pt'], row['q'], choice_lists[choices_key],
                    values, opts_list, {'atype': choices_key})
                questions.append(question)
                q += 1
        end_page(last_page)

        path = f'{dirname(__file__)}/survey-data/{key}-meta.json'
        with open(path) as json_file:
            meta = json.load(json_file)

        return cls(key, meta, pages)


def get_survey(key, choice_lists: Optional[Dict] = None) -> Survey:
    assert key in AVAILABLE_SURVEYS
    return Survey.factory(key, choice_lists)
