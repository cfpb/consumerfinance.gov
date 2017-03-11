from __future__ import unicode_literals

import time

from django.apps import apps

from knowledgebase.models import QuestionCategory as QC
from knowledgebase.models import Question, Audience, UpsellItem, EnglishAnswer
from ask_cfpb.models import (
    Answer,
    Category,
    NextStep,
    SubCategory)
from ask_cfpb.models import Audience as ASK_audience
from v1.util.migrations import get_or_create_page

PARENT_MAP = {
    'english_parent': {'slug': 'ask-cfpb',
                       'title': 'Ask CFPB',
                       'parent_slug': 'cfgov',
                       'language': 'en'},
    'spanish_parent': {'slug': 'inicio',
                       'title': 'Inicio',
                       'parent_slug': 'cfgov',
                       'language': 'es'},
    'spanish_subparent': {'slug': 'obtener-respuestas',
                          'title': 'Obtener respuestas',
                          'parent_slug': 'inicio',
                          'language': 'es'},
}


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
    time.sleep(2)


def get_kb_statuses(ask_id):
    q = Question.objects.get(id=ask_id)
    return {'en': (q.get_english_answer_state() == 'APPROVED'),
            'es': (q.get_spanish_answer_state() == 'APPROVED')}


def create_answer_pages(queryset):
    counter = 0
    if queryset:
        for answer in queryset:
            kb_statuses = get_kb_statuses(answer.id)
            for lang in ['en', 'es']:
                if kb_statuses[lang]:
                    _page = answer.create_or_update_page(language=lang)
                    revision = _page.get_latest_revision()
                    revision.publish()
                    counter += 1
    else:
        print("No Answer objects found in queryset.")
    print("\nCreated and published {} Answer pages.".format(counter))


def create_pages():
    time.sleep(2)
    print("Creating Answer pages ...")
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
        answer_base.answer = en_answer.answer.strip()
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
        if counter % 100 == 0:
            print("{}".format(counter))
        migrate_answer(question)
    print("Migrated or updated {} answers.".format(counter))


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
    print("Found {} Audience objects; needed to migrate {}\n"
          "Created {} Audience links".format(
              Audience.objects.count(),
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


def migrate_knowledgebase():
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
