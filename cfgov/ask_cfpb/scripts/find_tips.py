# An exploration of polluted knowledgebase code
import re

from bs4 import BeautifulSoup as bs

from ask_cfpb.models import Answer

TIPS = {}

COUNT_TABLE = """
Module   | bad styling | proper styling
:-----   | :---------- | :-------------
Tip      | {}          | {}
Warning  | {}          | {}
"""


def find_styled_divs(answer):
    soup = bs(answer, 'lxml')
    return soup.findAll('div', {'class': 'answer-module'})


def find_styled_modules():
    answers = Answer.objects.all()
    for answer in answers:
        tip_styled_divs = find_styled_divs(answer.answer)
        if tip_styled_divs:
            TIPS[answer.id] = len(tip_styled_divs)
    module_ct = 0
    for key in TIPS:
        module_ct += TIPS[key]
    print("We found {} styled tips and warnings.\n"
          "{} of our {} answers had a styled tip or warning.".format(
              module_ct, len(TIPS), answers.count()))


def get_style_counts(answer_text, heading):
    bad_count = len([m for m in re.finditer(
        '<strong>{}'.format(heading), answer_text)])
    good_count = len([m for m in re.finditer(
        '<h4>{}'.format(heading), answer_text)])
    return {'bad': bad_count,
            'good': good_count}


def count_stylings():
    COUNTS = {'bad_Warning': 0,
              'styled_Warning': 0,
              'bad_Tip': 0,
              'styled_Tip': 0}
    answers = Answer.objects.all()
    for heading in ['Warning', 'Tip']:
        for answer in answers:
            style_counts = get_style_counts(answer.answer, heading)
            COUNTS['bad_{}'.format(heading)] += style_counts['bad']
            COUNTS['styled_{}'.format(heading)] += style_counts['good']
    print(COUNT_TABLE.format(
        COUNTS['bad_Tip'],
        COUNTS['styled_Tip'],
        COUNTS['bad_Warning'],
        COUNTS['styled_Warning']))
