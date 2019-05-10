# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.utils.text import slugify

import unicodecsv

from ask_cfpb.models import AnswerPage
from v1.models import PortalTopic
from v1.models.snippets import GlossaryTerm


PROJECT_ROOT = settings.PROJECT_ROOT
CSV_PATH = "{}/ask_cfpb/fixtures/glossary_terms.csv".format(PROJECT_ROOT)


def run():
    with open(CSV_PATH, 'rU') as f:
        reader = unicodecsv.DictReader(f)
        for row in reader:
            # Get existing glossary term based on English term name
            name_en = row['NAME_EN']
            if not name_en:
                continue
            name_en = name_en.strip()
            topic = row['TOPIC'].strip()
            portal_topic = PortalTopic.objects.get(heading=topic)
            glossary_term = GlossaryTerm.objects.filter(
                name_en=name_en, portal_topic=portal_topic).first()

            # Populate glossary term with Spanish fields from CSV
            name_es = row['NAME_ES']
            glossary_term.name_es = name_es.strip()

            # For the definition, use the answer page's short answer
            # if there's an existing reference to an answer page
            if glossary_term.answer_page_en:
                answer_page_es = AnswerPage.objects.get(
                    answer_base__id=row['ANSWER_ID'],
                    language='es')
                glossary_term.answer_page_es = answer_page_es
                glossary_term.definition_es = answer_page_es.short_answer
            # Otherwise, populate it from CSV
            else:
                glossary_term.definition_es = row['DEFINITION_ES']

            glossary_term.anchor_es = slugify(name_es)
            glossary_term.save()
