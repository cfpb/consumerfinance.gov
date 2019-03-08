from __future__ import unicode_literals

import datetime
import os

from django.contrib.auth.models import User

from taggit.models import Tag

from ask_cfpb.models.django import NextStep
from ask_cfpb.models.pages import AnswerPage
from v1.models.snippets import RelatedResource


# A mapping of Audience pks to Tag pks
AUDIENCE_MAPPING = {
    3: 99,  # 'Older Americans': {'audience': 3, 'tag': 99}
    7: 102,  # 'Parents': {'audience': 7, 'tag': 102}
    5: 64,  # 'Servicemembers': {'audience': 5, 'tag': 64}
    1: 14  # 'Students': {'audience': 1, 'tag': 14}
}


def run():
    starter = datetime.datetime.now()
    migration_user_pk = os.getenv('MIGRATION_USER_PK', 9999)
    user = User.objects.filter(id=migration_user_pk).first()
    for next_step in NextStep.objects.all():
        RelatedResource.objects.get_or_create(
            title=next_step.title,
            text=next_step.text)

    for page in AnswerPage.objects.all():
        # Capture whether the page we're working with is a draft or not.
        # Our changes to 'live' and 'live + draft' pages can be published.
        draft = False
        if page.status_string == 'draft':
            draft = True

        # First, publish the page so we're working with the latest revision.
        # We'll unpublish draft pages at the end of this script.
        page.get_latest_revision().publish()
        page = AnswerPage.objects.get(pk=page.pk)

        # Then, migrate data from Answer to AnswerPage
        for category in page.answer_base.category.all():
            page.category.add(category)
        for subcategory in page.answer_base.subcategory.all():
            page.subcategory.add(subcategory)
        for audience in page.answer_base.audiences.all():
            page.tags.add(
                Tag.objects.get(pk=AUDIENCE_MAPPING[audience.pk]))
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

        # Save & publish our changes
        page.save_revision(user=user).publish()

        # Unpublish pages that were originally draft only
        if draft:
            page.unpublish()
    print("Migration took {}.".format(datetime.datetime.now() - starter))
