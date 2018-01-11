from itertools import chain
from django.apps import apps
from django.db import connections
from django.core.exceptions import ValidationError

from wagtail.wagtailcore.models import Page, PageRevision

from ask_cfpb.models.django import Category, SubCategory, Answer, Audience

from jobmanager.models.django import JobCategory, JobRegion
from reversion.models import Revision, Version
from v1.models.base import CFGOVAuthoredPages, CFGOVTaggedPages
from v1.models.snippets import Resource

SEEN_MODELS = []
PAGES_NOT_IMPORTED = []


def save_to_postgres(obj, **extra_save_options):
    obj.save(using='postgres', **extra_save_options)


def obliterate(*table_names):
    pg_cursor = connections['postgres'].cursor()
    for table_name in table_names:
        pg_cursor.execute('delete from %s' % table_name)


def copy_models_to_postgres(*models):
    for model in models:
        extra_save_options = {}

        # when importing a Page, we create all of the inherited tables
        # for the specific type, so no reason to process Page subclasses
        # here
        if issubclass(model, Page) and model is not Page:
            continue
        if model not in SEEN_MODELS:
            # batch_migrate(model)
            print "importing %s" % repr(model)
            model.objects.using('postgres').delete()
            for obj in model.objects.using('default').all():

                if isinstance(obj, CFGOVTaggedPages):
                    try:
                        obj.content_object
                    except Page.DoesNotExist:
                        continue
                if isinstance(obj, Answer):
                    extra_save_options['skip_page_update'] = True

                if isinstance(obj,PageRevision):
                    try:
                        obj.page
                    except Page.DoesNotExist:
                        continue

                if isinstance(obj, Page):
                    obj = obj.specific
                    # numchild numbers seem to screw with the save
                    # so let's just zero them out
                    obj.numchild = 0

                    try:
                        save_to_postgres(obj, **extra_save_options)
                    except ValidationError as e:
                        # there are some pages in the Trash with
                        # duplicate slugs (somehow)
                        # we'll "fix" the slug and try again
                        if 'slug' in e.error_dict:
                            obj.slug = obj.slug + str(obj.pk)
                            save_to_postgres(obj, **extra_save_options)
                            continue
                        else:
                            raise
                try:
                    save_to_postgres(obj, **extra_save_options)
                except:
                    import pdb;pdb.set_trace()

            for m2mfield in model._meta.many_to_many:
                m2m_model = getattr(model, m2mfield.name).through
                copy_models_to_postgres(m2m_model)
        SEEN_MODELS.append(model)
def run():
    # Even with --no-initial-data, there's still some tables we need
    # to zap before we can start populating the DB
    # This also helps with overwriting previous imports
    SEEN_MODELS.append(CFGOVAuthoredPages)
    SEEN_MODELS.append(Revision)
    SEEN_MODELS.append(Version)
    obliterate('ask_cfpb_answerlandingpage','v1_landingpage',
               'v1_sublandingpage',
               'data_research_mortgageperformancepage',
               'v1_browsepage',
               'v1_homepage',
               'v1_learnpage',
               'v1_eventpage',
               'v1_documentdetailpage',
               'v1_newsroompage',
               'v1_blogpage',
               'v1_legacynewsroompage',
               'v1_legacyblogpage',
               'v1_abstractfilterpage',
               'v1_activitylogpage',
               'v1_sublandingfilterablepage',
               'v1_eventarchivepage',
               'v1_newsroomlandingpage',
               'v1_browsefilterablepage',
               'jobmanager_emailapplicationlink',
               'jobmanager_usajobsapplicationlink',
               'jobmanager_gradepanel',
               'jobmanager_joblistingpage',
               'ask_cfpb_tagresultspage',
               'ask_cfpb_answerresultspage',
               'ask_cfpb_answercategorypage',
               'ask_cfpb_answerpage',
               'ask_cfpb_answeraudiencepage',
               'v1_cfgovtaggedpages',
               'v1_cfgovpagecategory',
               'v1_cfgovpage',
               'wagtailsharing_sharingsite',
               'wagtailcore_grouppagepermission',
               'wagtailcore_site',
               'wagtailcore_pagerevision',
               'wagtailredirects_redirect',
               'wagtailinventory_pageblock',
               'v1_feedback',
               'wagtailcore_page',
               )

    priority_models = apps.get_app_config('contenttypes').get_models()
    priority_models = chain(priority_models,
                            apps.get_app_config('auth').get_models(),
                            )
    copy_models_to_postgres(*priority_models)
    copy_models_to_postgres(JobCategory, JobRegion, Category, SubCategory,
                            Answer, Audience, Page, Resource)
    all_models = apps.get_models(include_auto_created=True)
    copy_models_to_postgres(*all_models)

