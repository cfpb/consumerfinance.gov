# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging
import re
import sys
import time
from six import text_type as unicode

from django.apps import apps
from django.core.management import call_command
from django.template.defaultfilters import slugify

from wagtail.wagtailcore.blocks.stream_block import StreamValue

import pytz
from bs4 import BeautifulSoup as bs
from knowledgebase.models import (
    Audience, EnglishAnswer, Question, QuestionCategory as QC, UpsellItem
)

from ask_cfpb.models import (
    Answer, Audience as ASK_audience, Category, NextStep, SubCategory
)
from v1.util.migrations import get_or_create_page


TZ = pytz.timezone('US/Eastern')

# Go live is 11 a.m. Wednesday, June 14, 2017
GO_LIVE_AT = datetime.datetime(2017, 6, 14, 11, 0, tzinfo=TZ)

logging.basicConfig(level=logging.WARNING)
logging.disable(logging.INFO)

FEATURED_ANSWER_IDS = {
    763: 1,
    779: 2,
    1023: 1,
    1145: 2,
    44: 1,
    61: 2,
    311: 1,
    316: 2,
    1397: 1,
    1695: 2,
    1641: 1,
    1679: 2,
    1161: 1,
    1507: 2,
    100: 1,
    122: 2,
    1567: 1,
    1589: 2,
    503: 1,
    545: 1,
    601: 2
}

utf8_swap_chars = {
    b'\xC2\x91': b"'",
    b'\xC2\x92': b"'",
    b'\xC2\x93': b'"',
    b'\xC2\x94': b'"',
    b'\xC2\x96': b'-',
    b'\xE2\x80\x8B': b'',  # ZERO WIDTH SPACE
    b'\xE2\x97\xA6': b'- ',  # small hollow circle
    b'\xEF\x82\xA7': b'- ',  # hollow box
}

unicode_swap_chars = {
    '\x91': "'",
    '\x92': "'",
    '\x93': '"',
    '\x94': '"',
    '\x96': '-',
    '\u200b': '',  # ZERO WIDTH SPACE
    '\u25e6': '- ',  # small hollow circle
    '\u25cb': '- ',  # alternate small hollow circle
    '\uf0a7': '',  # hollow box
}


def replace_utf8_chars(match):
    char = match.group(0)
    return utf8_swap_chars[char]


def replace_unicode_chars(match):
    char = match.group(0)
    return unicode_swap_chars[char]


def clean_utf8(utf8_string):
    return re.sub(
        b'(' + b'|'.join(utf8_swap_chars.keys()) +
        b')', replace_utf8_chars, utf8_string)


def clean_unicode(unicode_string):
    return re.sub(
        '(' + '|'.join(unicode_swap_chars.keys()) +
        ')', replace_unicode_chars, unicode_string)


def unwrap_soup(soup):
    soup.html.unwrap()
    soup.body.unwrap()
    return unicode(soup)


def convert_divs_to_asides(answer_text):
    soup = bs(answer_text, 'lxml')
    for div in soup.findAll('div', {'class': 'answer-module'}):
        div.name = 'aside'
    return unwrap_soup(soup)


def clean_orphan_tips(answer_text):
    headings = ['TIP', 'WARNING', 'NOTE']
    soup = bs(answer_text.replace('<br/><br/>', '</p><p>'), 'lxml')
    # wrap any orphan h4 tip headings
    h4s = soup('h4')
    for hed in h4s:
        if hed.parent.name == 'p' and hed.text.strip(':').upper() in headings:
            wrapper = hed.parent.wrap(
                soup.new_tag('aside'))
            wrapper['class'] = 'answer-module'
    strongs = soup('strong')
    for strong in strongs:
        # clean out spans
        if strong('span'):
            for span in strong('span'):
                span.unwrap()
        # turn strong tips into h4 and wrap in aside
        if strong.text.strip(':').upper() in headings:
            strong.name = 'h4'
            if strong.parent.name == 'p':
                wrapper = strong.parent.wrap(
                    soup.new_tag('aside'))
                wrapper['class'] = 'answer-module'
                if ':' in wrapper.contents:
                    i = wrapper.contents.index(':')
                    del(wrapper.contents[i])
    return unwrap_soup(soup)


def fix_tips(answer_text):
    clean1 = convert_divs_to_asides(answer_text)
    clean2 = clean_orphan_tips(clean1)
    return clean2


# PAGE CREATION

def prep_page(page, go_live_date=False):
    """Set the go-live date, create a revision, save page, publish revision"""
    page.has_unpublished_changes = True
    if go_live_date:
        page.go_live_at = GO_LIVE_AT
    revision = page.save_revision()
    page.save()
    revision.publish()


def get_or_create_landing_pages():
    """
    Create Spanish and English landing pages.
    """

    from v1.models import CFGOVPage, LandingPage
    en_root = CFGOVPage.objects.get(slug='cfgov').specific
    es_root = LandingPage.objects.get(slug='es').specific

    hero_stream_value = [
        {'type': 'hero',
         'value': {
             'heading': 'Ask CFPB',
             'links': [],
             'background_color': '#ffffff',
             'body': ('We offer clear, impartial answers to hundreds '
                      'of financial questions. Find the information you need '
                      'to make more informed choices about your money.')}}]
    landing_map = {
        'en': {'slug': 'ask-cfpb',
               'title': 'Ask CFPB',
               'hero': hero_stream_value,
               'parent': en_root},
        'es': {'slug': 'obtener-respuestas',
               'title': 'Obtener respuestas',
               'hero': None,
               'parent': es_root}
    }
    counter = 0
    for language in sorted(landing_map.keys()):
        _map = landing_map[language]
        landing_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerLandingPage',
            _map['title'],
            _map['slug'],
            _map['parent'],
            language=language)
        if _map['hero']:
            stream_block = landing_page.header.stream_block
            landing_page.header = StreamValue(
                stream_block,
                _map['hero'],
                is_lazy=True)
        prep_page(landing_page)
        time.sleep(1)
        counter += 1

    print("Created an 'es' parent and {} landing pages".format(counter))


def get_or_create_search_results_pages():
    from v1.models import CFGOVPage
    parent_en = CFGOVPage.objects.get(slug='ask-cfpb').specific
    parent_es = CFGOVPage.objects.get(slug='obtener-respuestas').specific
    language_map = {
        'en': {'title': 'Ask CFPB search results',
               'slug': 'ask-cfpb-search-results',
               'page_type': 'AnswerResultsPage',
               'language': 'en',
               'parent': parent_en},
        'es': {'title': 'Respuestas',
               'slug': 'respuestas',
               'page_type': 'AnswerResultsPage',
               'language': 'es',
               'parent': parent_es},
        'tag': {'title': 'Buscar por etiqueta',
                'slug': 'buscar-por-etiqueta',
                'page_type': 'TagResultsPage',
                'language': None,
                'parent': parent_es}
    }
    counter = 0
    for key in language_map:
        _map = language_map[key]
        results_page = get_or_create_page(
            apps,
            'ask_cfpb',
            _map['page_type'],
            _map['title'],
            _map['slug'],
            _map['parent'])
        if _map['language']:
            results_page.language = _map['language']
        prep_page(results_page)
        time.sleep(1)
        counter += 1
    print("Created {} search results pages".format(counter))


def get_or_create_category_pages():
    from v1.models import CFGOVPage
    parent = CFGOVPage.objects.get(slug='ask-cfpb').specific
    counter = 0
    for cat in Category.objects.all():
        for language in ['en', 'es']:
            if language == 'en':
                title = cat.name
                page_slug = "category-{}".format(cat.slug)
                parent = CFGOVPage.objects.get(slug='ask-cfpb').specific
            else:
                title = cat.name_es
                page_slug = "categoria-{}".format(cat.slug_es)
                parent = CFGOVPage.objects.get(
                    slug='obtener-respuestas').specific

            cat_page = get_or_create_page(
                apps,
                'ask_cfpb',
                'AnswerCategoryPage',
                title,
                page_slug,
                parent,
                language=language,
                ask_category=cat)
            prep_page(cat_page)
            time.sleep(1)
            counter += 1
    print("Created {} category pages".format(counter))


def get_or_create_audience_pages():
    from v1.models import CFGOVPage
    parent = CFGOVPage.objects.get(slug='ask-cfpb').specific
    counter = 0
    for audience in ASK_audience.objects.all():
        audience_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerAudiencePage',
            audience.name,
            "audience-{}".format(slugify(audience.name)),
            parent,
            language='en',
            ask_audience=audience)
        prep_page(audience_page)
        time.sleep(1)
        counter += 1
    print("Created {} audience pages".format(counter))


def get_kb_statuses(ask_id):
    q = Question.objects.get(id=ask_id)
    return {'en': (q.get_english_answer_state() == 'APPROVED'),
            'es': (q.get_spanish_answer_state() == 'APPROVED')}


def create_answer_pages(queryset):
    count = 0
    count_en = 0
    count_es = 0
    if queryset:
        for answer in queryset:
            kb_statuses = get_kb_statuses(answer.id)
            for lang in ['en', 'es']:
                if kb_statuses[lang]:
                    count += 1
                    _page = answer.create_or_update_page(language=lang)
                    if lang == 'en':
                        count_en += 1
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    elif lang == 'es':
                        count_es += 1
                        sys.stdout.write('+')
                        sys.stdout.flush()
                    _page.go_live_at = GO_LIVE_AT
                    revision = _page.save_revision(
                        approved_go_live_at=GO_LIVE_AT)
                    revision.publish()
    else:
        print("No Answer objects found in queryset.")
    print("\nCreated and published {} Answer pages.\n"
          "  English: {}\n"
          "  Spanish: {}".format(count, count_en, count_es))


def create_pages():
    print("Creating Answer pages: . = English, + = Spanish")
    create_answer_pages(Answer.objects.all())


# ANSWER AND METADATA CREATION

def migrate_categories():
    """Move parent QuestionCategories into the new Category model"""
    topics = QC.objects.filter(parent=None)
    create_count = 0
    update_count = 0
    for qc in topics:
        cat, cr = Category.objects.get_or_create(
            slug=qc.slug,
            slug_es=qc.slug_es,
            name=qc.name,
            name_es=qc.name_es,
            intro=qc.description,
            intro_es='')
        if cr:
            create_count += 1
        else:
            update_count += 1
    print("Found {} topic categories, "
          "created {} "
          "and updated {}".format(
              topics.count(), create_count, update_count))


def get_en_answer(question, cats, en_answer):
    answer, created = Answer.objects.get_or_create(
        id=question.id,
        slug=en_answer.slug)
    for cat in cats:
        answer.category.add(cat)
    answer.last_edited = question.updated_at.date()
    answer.question = clean_unicode(en_answer.title.strip())
    return answer


def get_es_answer(question, cats, es_answer):
    answer, created = Answer.objects.get_or_create(
        id=question.id,
        slug_es=es_answer.slug)
    for cat in cats:
        answer.category.add(cat)
    answer.created_at = question.created_at
    answer.last_edited_es = question.updated_at.date()
    answer.question_es = clean_unicode(es_answer.title.strip())
    return answer


def fill_out_es_answer(question, answer, es_answer):
    answer.slug_es = es_answer.slug
    answer.question_es = es_answer.title.strip()
    answer.answer_es = clean_unicode(es_answer.answer.strip())
    answer.last_edited_es = question.updated_at.date()
    answer.snippet_es = ''
    answer.search_tags_es = es_answer.tagging
    return answer


def build_answer(question, cats, en_answer=None, es_answer=None):
    if en_answer:
        answer_base = get_en_answer(question, cats, en_answer)
        answer_base.answer = clean_unicode(fix_tips(en_answer.answer.strip()))
        answer_base.last_edited = question.updated_at.date()
        answer_base.snippet = en_answer.one_sentence_answer.strip()
        answer_base.search_tags = en_answer.tagging
        for cat in cats:
            answer_base.category.add(cat)
        for qc in question.question_category.exclude(parent=None):
            answer_base.subcategory.add(
                SubCategory.objects.get(slug=qc.slug))
        if es_answer:
            answer_base = fill_out_es_answer(question, answer_base, es_answer)
    elif es_answer:  # no English answer to be had
        answer_base = get_es_answer(question, cats, es_answer)
        answer_base = fill_out_es_answer(question, answer_base, es_answer)
    else:  # no answers for this question yet, so we'll save with an ID slug
        answer_base, created = Answer.objects.get_or_create(
            id=question.id,
            slug="answer-{}".format(question.id))
        for cat in cats:
            answer_base.category.add(cat)
    return answer_base


def migrate_answer(question):
    parents = question.question_category.filter(parent=None)
    cats = Category.objects.filter(
        slug__in=[parent.slug for parent in parents])
    answer = build_answer(
        question,
        cats,
        question.get_english_answer(),
        question.get_spanish_answer())
    if answer:
        answer.save()


def migrate_questions():
    queryset = Question.objects.all()
    print("Migrating {} KB questions ...".format(queryset.count()))
    counter = 0
    for question in queryset:
        counter += 1
        if counter % 250 == 0:
            print("{}".format(counter))
        migrate_answer(question)
    print("Migrated {} answers.".format(counter))


def migrate_audiences():
    audiences_created = 0
    audience_relation_count = 0
    for audience in Audience.objects.all():
        new_audience, cr = ASK_audience.objects.get_or_create(
            id=audience.id,
            name=audience.name)
        if cr:
            audiences_created += 1
    for question in Question.objects.all():
        ask_cfpb_answer = Answer.objects.get(id=question.id)
        for audience in question.audiences.all():
            ask_cfpb_answer.audiences.add(
                ASK_audience.objects.get(id=audience.id))
            audience_relation_count += 1
    print("Migrated {} Audience objects\n"
          "Found {} already created\n"
          "Created {} Audience links".format(
              audiences_created,
              Audience.objects.count(),
              audience_relation_count))


def migrate_next_steps():
    """Move knowledgebase UpsellItems to ask_cfpb NextSteps"""
    upsells_created = 0
    upsells_updated = 0
    nextsteps_linked = 0
    upsells = UpsellItem.objects.all()
    print("Migrating {} UpsellItems to the NextStep model ...".format(
        upsells.count()))
    for upsell in upsells:
        nextstep, cr = NextStep.objects.get_or_create(
            id=upsell.id,
            title=upsell.title)
        nextstep.show_title = upsell.show_title
        nextstep.text = upsell.text
        nextstep.save()
        if cr:
            upsells_created += 1
        else:
            upsells_updated += 1
    print("Created {} NextStep objects "
          "and updated {}".format(upsells_created, upsells_updated))
    print("Adding NextStep links ...")
    for ea in EnglishAnswer.objects.all():
        if ea.upsellitem:
            answer = Answer.objects.get(id=ea.question.id)
            answer.next_step = NextStep.objects.get(id=ea.upsellitem.id)
            answer.save()
            nextsteps_linked += 1
    print("Created {} NextStep links".format(nextsteps_linked))


def migrate_subcategories():
    """Put QuestionCategories that aren't parents into new SubCategory Model"""
    subcategories = QC.objects.exclude(parent=None)
    create_count = 0
    update_count = 0
    for qc in subcategories:
        subcat, cr = SubCategory.objects.get_or_create(
            id=qc.id,
            name=qc.name,
            name_es=qc.name_es,
            slug=qc.slug,
            slug_es=qc.slug_es)
        subcat.featured = qc.featured
        subcat.weight = qc.weight
        subcat.description = qc.description
        subcat.more_info = qc.more_info
        subcat.parent = Category.objects.get(slug=qc.parent.slug)
        subcat.save()
        if cr:
            create_count += 1
        else:
            update_count += 1
    print("Created {} ASK categories "
          "and updated {}".format(create_count, update_count))


def add_related_categories():
    update_count = 0
    for cat in QC.objects.exclude(parent=None):
        subcategory = SubCategory.objects.get(id=cat.id)
        for related in cat.related_subcategories.exclude(parent=None):
            subcategory.related_subcategories.add(
                SubCategory.objects.get(id=related.id))
        subcategory.save()
        update_count += 1
    print("Updated related categories for {} ASK categories.").format(
        update_count)


def add_related_questions():
    update_count = 0
    print("Adding related_question links ...")
    for q in Question.objects.exclude(related_questions=None):
        answer = Answer.objects.get(id=q.id)
        for related in q.related_questions.all():
            update_count += 1
            answer.related_questions.add(Answer.objects.get(id=related.id))
        answer.save()
    print("Added {} related_question relations".format(update_count))


def clean_up_blank_answers():
    start_count = Answer.objects.count()
    Answer.objects.filter(answer='', answer_es='').delete()
    print("Cleaned up {} blank answers".format(
        start_count - Answer.objects.count()))


def set_featured_ids():
    featured = Answer.objects.filter(id__in=FEATURED_ANSWER_IDS)
    for answer in featured:
        answer.featured = True
        answer.featured_rank = FEATURED_ANSWER_IDS[answer.id]
        answer.save()
    print("Marked {} answers as 'featured'".format(featured.count()))


def run():
    migrate_categories()
    migrate_subcategories()
    add_related_categories()
    migrate_questions()
    migrate_audiences()
    migrate_next_steps()
    add_related_questions()
    set_featured_ids()
    clean_up_blank_answers()
    get_or_create_landing_pages()
    get_or_create_category_pages()
    get_or_create_audience_pages()
    get_or_create_search_results_pages()
    create_pages()
    logging.disable(logging.NOTSET)
    call_command('update_index', 'ask_cfpb', r=True)
