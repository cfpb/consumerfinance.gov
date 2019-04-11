from __future__ import unicode_literals

import os

from django.contrib.auth.models import User

from bs4 import BeautifulSoup as bs

from ask_cfpb.models.pages import AnswerPage


tags = ['em', 'i', 'strong', 'b']

false_positives = [1637]


def run():
    answers = [
        p for p in AnswerPage.objects.filter(language='es', redirect_to=None)
        if p.status_string != 'draft'
    ]
    migration_user_pk = os.getenv('MIGRATION_USER_PK', 9999)
    user = User.objects.filter(id=migration_user_pk).first()
    updated = 0
    for page in answers:
        soup = bs(page.answer, "html.parser")
        first_paragraph = soup.p
        paragraph_content = first_paragraph.text
        has_short_answer = False
        if first_paragraph:
            for tag in tags:
                tag_instances = first_paragraph.findAll(tag)
                if len(tag_instances):
                    result = ''.join(i.text for i in tag_instances)
                    if (
                            result.strip() == paragraph_content.strip()
                            and page.answer_base.id not in false_positives):
                        for i in tag_instances:
                            i.unwrap()
                        page.short_answer = first_paragraph
                        has_short_answer = True
            if has_short_answer:
                updated += 1
                soup.p.extract()
                page.answer = soup
                page.save_revision(user=user).publish()
    print('Migrated {} Spanish short answers'.format(updated))
