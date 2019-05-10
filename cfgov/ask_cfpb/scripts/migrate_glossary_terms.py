# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.utils.text import slugify

import unicodecsv
from bs4 import BeautifulSoup as bs

from ask_cfpb.models import AnswerPage
from v1.models import CFGOVPage, PortalTopic
from v1.models.snippets import GlossaryTerm
from v1.models.sublanding_page import SublandingPage


PROJECT_ROOT = settings.PROJECT_ROOT
CSV_PATH = "{}/ask_cfpb/fixtures/glossary_terms.csv".format(PROJECT_ROOT)


def run():
    for page in CFGOVPage.objects.filter(slug='key-terms'):
        parent = page.get_parent().specific
        if parent.__class__ == SublandingPage and parent.portal_topic:
            create_terms_key_terms_page(
                page=page,
                portal_topic=parent.portal_topic)

    create_terms_answer_pages()


def create_terms_key_terms_page(page, portal_topic):
    """
    Parses the terms & definitions on a given key terms page,
    and creates new glossary term snippets out of them.
    """
    for block in page.specific.content:
        if block.block_type != 'full_width_text':
            continue
        for child in block.value:
            if child.block_type == 'content':
                contents = bs(child.value.source, 'html.parser')
                headings = contents.find_all('h3')
                for h3 in headings:
                    if h3.text:
                        h3_contents = bs(h3.contents[0], 'html.parser')
                        div = h3_contents.find('div')
                        term = div.text.strip()
                        definition = ''
                        sibling = h3.next_sibling
                        while sibling and sibling.name != 'h3':
                            if sibling.text:
                                definition += sibling.encode(formatter="html")
                            sibling = sibling.next_sibling
                        glossary_term = GlossaryTerm(
                            name_en=term,
                            definition_en=definition,
                            portal_topic=portal_topic,
                            anchor_en=slugify(term),
                        )
                        glossary_term.save()


def create_terms_answer_pages():
    with open(CSV_PATH, 'rU') as f:
        reader = unicodecsv.DictReader(f)
        for row in reader:
            name_en = row['NAME_EN']
            if not name_en:
                continue
            name_en = name_en.strip()
            if row['ANSWER_ID'] == '':
                continue
            topic = row['TOPIC'].strip()
            portal_topic = PortalTopic.objects.get(heading=topic)
            existing_term = GlossaryTerm.objects.filter(
                name_en=name_en, portal_topic=portal_topic)
            if existing_term:
                continue
            answer_page_en = AnswerPage.objects.get(
                answer_base__id=row['ANSWER_ID'],
                language='en')
            glossary_term = GlossaryTerm(
                name_en=name_en,
                definition_en=answer_page_en.short_answer,
                portal_topic=portal_topic,
                answer_page_en=answer_page_en,
                anchor_en=slugify(name_en),
            )
            glossary_term.save()
