"""Objects for creating surveys

A Survey object has a set of pages and questions within those to model
a complete survey. A set of Django form classes can be generated to
represent all the survey pages (assembled by SurveyWizard), and the
survey can be scored by passing it the full set of answers.

The surveys are configured via CSV files (in code) and some templates
define content that appears above certain pages.
"""

import csv
import hashlib
import json
from os.path import dirname
from typing import Any, Dict, List, Optional, Tuple

from django import forms

from teachers_digital_platform.forms import SurveyForm, markup

# If True, all the best scoring answers will be auto-selected.
PREFILL_ANSWERS = False

# Which survey keys will be made available.
AVAILABLE_SURVEYS = ("3-5", "6-8", "9-12")

ITEM_SEPARATOR = "‣"


def _question_row(row: Dict[str, str]):
    """
    Transform the keys of each question CSV row. If the CSV headers change,
    this will make a single place to fix it.
    """
    return {
        "q": row["Question"],
        "pt": row["Part"],
        "pg": row["Page"],
        "a": row["Answer type"],
        "w": row["Answer worth"],
        "s": row["Section"],
    }


def _answer_types_row(row: Dict[str, str]):
    """
    Transform the keys of each answer-type CSV row. If the CSV headers
    change, this will make a single place to fix it.
    """
    return {
        "k": row["Key"],
        "c": row["Choices"],
    }


class ChoiceList:
    """
    A set of choices to be presented on a question. A single object can
    be re-used for many questions to save memory.
    """

    def __init__(self, labels: List[str]):
        self.labels = labels
        self.choices = tuple((str(k), v) for k, v in enumerate(labels))

    @classmethod
    def from_string(cls, s: str, lookup: Dict):
        """Convert a string like 'Foo | Bar | Bing' into a new ChoiceList"""
        labels = list(x.strip() for x in s.split("|"))

        # Allow references like: [list:Foo]
        for k, v in enumerate(labels):
            if v[0:6] == "[list:" and v[-1] == "]":
                possible_ref = v[6:-1]
                if possible_ref in lookup:
                    joiner = f" {ITEM_SEPARATOR} "
                    labels[k] = joiner.join(lookup[possible_ref].labels)

        return cls(labels)

    @classmethod
    def get_all(cls):
        """Get a list of all available ChoiceLists from CSV"""
        ret: Dict[str, cls] = {}

        path = f"{dirname(__file__)}/survey-data/answer-types.csv"
        with open(path, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_answer_types_row(row) for row in reader):
                ret[row["k"]] = cls.from_string(row["c"], ret)

        return ret


class Question:
    """
    Base question that can be scored
    """

    def __init__(self, num: int, part: str):
        self.key = f"q{num}"
        self.num = num
        self.part = part

    def get_score(self, answer):
        return 0

    def get_field(self):
        return None


class ChoiceQuestion(Question):
    """
    Choice question for displaying radio buttons
    """

    def __init__(
        self,
        num: int,
        part: str,
        label: str,
        choice_list: ChoiceList,
        answer_values: List[float],
        meta: Optional[Dict] = None,
    ):
        super().__init__(num, part)
        self.meta = {} if meta is None else meta
        self.choice_list = choice_list
        self.label = label
        self.answer_values = answer_values

    def get_choices(self) -> Tuple[Tuple[str, str], ...]:
        return self.choice_list.choices

    def get_score(self, answer) -> float:
        """Get a single score based on the answer index"""

        # formtools.NamedUrlCookieWizardView appears to have a bug where
        # valid answer data ("0"..."4") sometimes shows up in
        # all_cleaned_data as empty string. We can't really handle this
        # other than to grade with some valid response, below "0".
        if type(answer) is not str or not answer.isdecimal():
            answer = "0"

        answer = int(answer)
        assert answer >= 0
        assert answer < len(self.choice_list.labels)
        return self.answer_values[answer]

    def get_field(self):
        """Get a form field class to place this question in a form"""
        label = "".join(
            [
                markup('<strong class="question-num">'),
                str(self.num),
                ".",
                markup("</strong>"),
                " ",
                self.label,
            ]
        )

        initial = None
        if PREFILL_ANSWERS:
            initial = self.answer_values.index(max(self.answer_values))

        classes = ["ChoiceField", "tdp-survey__choice-question"]
        if "atype" in self.meta:
            atype = self.meta["atype"]
            classes.append(f"tdp-survey__atype-{atype}")

        widget = forms.RadioSelect({"class": " ".join(classes)})
        widget.template_name = "teachers_digital_platform/choice.html"

        return {
            "key": self.key,
            "field": forms.ChoiceField(
                widget=widget,
                choices=self.choice_list.choices,
                label=label,
                required=False,
                initial=initial,
            ),
        }


class SurveyPage:
    """
    Page of an survey
    """

    def __init__(self, questions: List[Question]):
        self.questions = questions

    def get_fields(self):
        """
        Get a Dict of form field classes that will comprise form attributes
        for a single page of the survey.
        """
        fields = {}

        for question in self.questions:
            obj = question.get_field()
            fields[obj["key"]] = obj["field"]

        return fields

    def get_score(self, all_cleaned_data):
        """
        Get the score total for this page and a dict of scores for each
        question.
        """
        total = 0
        question_scores = {}

        for question in self.questions:
            answer = all_cleaned_data[question.key]
            score = question.get_score(answer)
            total += score
            question_scores[question] = score

        return {
            "total": total,
            "question_scores": question_scores,
        }

    def get_form_class(self, name: str):
        """Build the form class for this page"""
        return type(
            name,
            (SurveyForm,),
            self.get_fields(),
        )


class Survey:
    """
    A full survey
    """

    ITEM_SEPARATOR = ITEM_SEPARATOR

    def __init__(
        self, key: str, meta: Dict[str, Any], pages: List[SurveyPage]
    ):
        self.key = key
        self.meta = meta
        self.pages = pages

    def num_questions_by_page(self) -> List[int]:
        """
        Get a list of how many questions appear on each page, for use in
        JavaScript for knowing the user's progress within the survey.
        """
        return list(len(page.questions) for page in self.pages)

    def get_score(self, all_cleaned_data) -> float:
        """
        Get the score total for this survey, each page, and and a dict of
        scores for all questions.
        """
        total = 0
        question_scores = {}
        page_scores = {}

        for page in self.pages:
            score = page.get_score(all_cleaned_data)
            subtotal = score["total"]
            page_scores[page] = subtotal
            question_scores.update(score["question_scores"])
            total += subtotal

        return {
            "question_scores": question_scores,
            "page_scores": page_scores,
            "total": total,
        }

    def adjust_total_score(self, total) -> float:
        """Adjust the total score so the top score is 100"""
        if "score_multiplier" not in self.meta:
            return total

        expr = self.meta["score_multiplier"]

        if isinstance(expr, (float, int)):
            return total * expr

        if type(expr) is list and len(expr) == 3 and expr[1] == "/":
            return total * expr[0] / expr[2]

        raise ValueError(f"score_multiplier {expr} is unsupported")

    def get_form_list(self):
        """Get a list of (page name, form class) tuples"""
        page_classes = []

        for page_i, page in enumerate(self.pages):
            name = f"p{page_i + 1}"

            # Unique class name for each survey + page (not technically
            # required but feels safer)
            hash = hashlib.md5((self.key + "|" + name).encode())
            classname = "FormPage" + hash.hexdigest()

            page_classes.append((name, page.get_form_class(classname)))

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
            page = SurveyPage(questions.copy())
            pages.append(page)
            questions.clear()

        path = f"{dirname(__file__)}/survey-data/{key}.csv"
        with open(path, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_question_row(row) for row in reader):
                if last_page is None:
                    last_page = row["pg"]
                if row["pg"] != last_page:
                    end_page(last_page)

                last_page = row["pg"]

                values = list(int(x.strip()) for x in row["w"].split(" "))

                choices_key = row["a"]
                if choices_key not in choice_lists:
                    msg = f"Unknown answer type {choices_key}"
                    raise NameError(msg)

                question = ChoiceQuestion(
                    q,
                    row["pt"],
                    row["q"],
                    choice_lists[choices_key],
                    values,
                    {"atype": choices_key},
                )
                questions.append(question)
                q += 1
        end_page(last_page)

        path = f"{dirname(__file__)}/survey-data/{key}-meta.json"
        with open(path) as json_file:
            meta = json.load(json_file)

        return cls(key, meta, pages)


def get_survey(key, choice_lists: Optional[Dict] = None) -> Survey:
    """Get a survey object by its key"""
    assert key in AVAILABLE_SURVEYS
    return Survey.factory(key, choice_lists)
