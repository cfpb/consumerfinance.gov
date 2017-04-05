from __future__ import unicode_literals

import sys
import time
import logging

from bs4 import BeautifulSoup as bs
from django.apps import apps
from wagtail.wagtailcore.blocks.stream_block import StreamValue

from knowledgebase.models import QuestionCategory as QC
from knowledgebase.models import Question, Audience, UpsellItem, EnglishAnswer
from ask_cfpb.models import (
    Answer,
    Category,
    NextStep,
    SubCategory)
from ask_cfpb.models import Audience as ASK_audience
from v1.util.migrations import get_or_create_page

logging.basicConfig(level=logging.WARNING)
logging.disable(logging.INFO)

PARENT_MAP = {
    'english_parent': {'slug': 'ask-cfpb',
                       'title': 'Ask CFPB',
                       'parent_slug': 'cfgov',
                       'language': 'en'},
    'spanish_parent': {'slug': 'obtener-respuestas',
                       'title': 'Obtener respuestas',
                       'parent_slug': 'cfgov',
                       'language': 'es'},
}


def add_feedback_module(page):
    stream_value = [
        {'type': 'feedback',
         'value': {'was_it_helpful_text': 'Was this page helpful to you?',
                   'button_text': 'Submit',
                   'intro_text': '',
                   'question_text': '',
                   'radio_intro': '',
                   'radio_text': ('This information helps us '
                                  'understand your question better.'),
                   'radio_question_1': 'How soon do you expect to buy a home?',
                   'radio_question_2': 'Do you currently own a home?',
                   'contact_advisory': ''}}]
    stream_block = page.content.stream_block
    page.content = StreamValue(stream_block, stream_value, is_lazy=True)
    page.save_revision()


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


def get_or_create_parent_pages():
    from v1.models import CFGOVPage
    counter = 0
    for parent_type in sorted(PARENT_MAP.keys()):
        _map = PARENT_MAP[parent_type]
        parent_page = get_or_create_page(
            apps,
            'v1',
            'LandingPage',
            _map['title'],
            _map['slug'],
            CFGOVPage.objects.get(slug=_map['parent_slug']).specific,
            language=_map['language'])
        parent_page.has_unpublished_changes = True
        revision = parent_page.save_revision()
        parent_page.save()
        revision.publish()
        time.sleep(1)
        counter += 1
    print("Created {} parent pages".format(counter))


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
                    revision = _page.get_latest_revision()
                    revision.publish()
                    _page.refresh_from_db()
                    add_feedback_module(_page)
                    revision = _page.get_latest_revision()
                    revision.publish()
    else:
        print("No Answer objects found in queryset.")
    print("\nCreated and published {} Answer pages.\n"
          "  English: {}\n"
          "  Spanish: {}".format(count, count_en, count_es))


def create_pages():
    print("Creating Answer pages: . = English, + = Spanish")
    create_answer_pages(Answer.objects.all())


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
    answer.question = en_answer.title.strip()
    return answer


def get_es_answer(question, cats, es_answer):
    answer, created = Answer.objects.get_or_create(
        id=question.id,
        slug_es=es_answer.slug)
    for cat in cats:
        answer.category.add(cat)
    answer.created_at = question.created_at
    answer.last_edited_es = question.updated_at.date()
    answer.question_es = es_answer.title.strip()
    return answer


def fill_out_es_answer(question, answer, es_answer):
    answer.slug_es = es_answer.slug
    answer.question_es = es_answer.title.strip()
    answer.answer_es = es_answer.answer.strip()
    answer.last_edited_es = question.updated_at.date()
    answer.snippet_es = ''
    return answer


def build_answer(question, cats, en_answer=None, es_answer=None):
    if en_answer:
        answer_base = get_en_answer(question, cats, en_answer)
        answer_base.answer = fix_tips(en_answer.answer.strip())
        answer_base.last_edited = question.updated_at.date()
        answer_base.snippet = en_answer.one_sentence_answer.strip()
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
          "Created {} Audience links".format(
              audiences_created,
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


def add_featured_questions():
    update_count = 0
    for cat in QC.objects.exclude(parent=None):
        subcategory = SubCategory.objects.get(id=cat.id)
        for featured in cat.featured_questions.all():
            subcategory.featured_questions.add(
                Answer.objects.get(id=featured.id))
        subcategory.save()
        update_count += 1
    print("Updated featured questions for {} ASK categories.").format(
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


def run():
    migrate_categories()
    migrate_subcategories()
    add_related_categories()
    migrate_questions()
    add_featured_questions()
    migrate_audiences()
    migrate_next_steps()
    add_related_questions()
    clean_up_blank_answers()
    get_or_create_parent_pages()
    create_pages()
    logging.disable(logging.NOTSET)
