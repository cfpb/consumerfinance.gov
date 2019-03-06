from __future__ import unicode_literals

from ask_cfpb.models.pages import AnswerPage


unsupported = ['\x92', '\x93', '\x94', '\x96']


def fix(text):
    text = text.replace('\x92', "'")
    text = text.replace('\x93', '"')
    text = text.replace('\x94', '"')
    text = text.replace('\x96', '-')
    return text


def run():
    for page in AnswerPage.objects.all():
        fixed = False

        for string in unsupported:
            if string in page.question:
                page.question = fix(page.question)
                fixed = True
            if string in page.answer:
                page.answer = fix(page.answer)
                fixed = True
            if string in page.snippet:
                page.snippet = fix(page.snippet)
                fixed = True

        if fixed:
            page.save_revision().publish()
