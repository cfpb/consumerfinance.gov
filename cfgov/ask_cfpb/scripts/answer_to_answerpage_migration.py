import os

from django.contrib.auth.models import User

from ask_cfpb.models.django import NextStep
from ask_cfpb.models.pages import AnswerPage
from v1.models.snippets import RelatedResource


def run():
    migration_user_pk = os.getenv('MIGRATION_USER_PK', 9999)
    user = User.objects.filter(id=migration_user_pk).first()
    for next_step in NextStep.objects.all():
        RelatedResource.objects.get_or_create(
            title=next_step.title,
            text=next_step.text)

    for page in AnswerPage.objects.all():
        for category in page.answer_base.category.all():
            page.category.add(category)
        for subcategory in page.answer_base.subcategory.all():
            page.subcategory.add(subcategory)

        if page.answer_base.next_step:
            page.related_resource = RelatedResource.objects.get(
                title=page.answer_base.next_step.title,
                text=page.answer_base.next_step.text)

        page.featured = page.answer_base.featured
        page.featured_rank = page.answer_base.featured_rank
        page.statement = page.answer_base.statement
        page.social_sharing_image = page.answer_base.social_sharing_image
        page.answer_id = page.answer_base.id

        if page.language == 'es':
            if page.redirect_to and page.redirect_to.spanish_page:
                page.redirect_to_page = page.redirect_to.spanish_page
            page.search_tags = page.answer_base.search_tags_es
            page.last_edited = page.answer_base.last_edited_es
            for related_question in page.answer_base.related_questions.all():
                page.related_questions.add(related_question.spanish_page)
        elif page.language == 'en':
            if page.redirect_to and page.redirect_to.english_page:
                page.redirect_to_page = page.redirect_to.english_page
            page.search_tags = page.answer_base.search_tags
            page.last_edited = page.answer_base.last_edited
            for related_question in page.answer_base.related_questions.all():
                page.related_questions.add(related_question.english_page)

        if page.status_string != 'draft':
            # We need to publish for the answer ID, next step, and search tags
            page.save_revision(user=user).publish()
        else:
            page.save_revision(user=user)
