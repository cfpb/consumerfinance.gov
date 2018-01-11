from itertools import chain
from django.apps import apps
from django.db import connections
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey

from taggit.models import TaggedItemBase
from wagtail.wagtailcore.models import Page, PageRevision

from reversion.models import Revision, Version

from v1.models.base import CFGOVAuthoredPages

SEEN_MODELS = []
PAGES_NOT_IMPORTED = []


def slow_save(*objects):
    for obj in objects:
        obj.save(using='postgres')


def obliterate(*table_names):
    pg_cursor = connections['postgres'].cursor()
    for table_name in table_names:
        pg_cursor.execute('delete from %s' % table_name)


def copy_models_to_postgres(*models):
    for model in models:

        # when importing a Page, we create all of the inherited tables
        # for the specific type, so no reason to process Page subclasses
        # here

        if model not in SEEN_MODELS:
            SEEN_MODELS.append(model)

            # skip proxy models
            if model._meta.proxy:
                continue

            # first, load tables needed to satisfy foreign keys
            for field in model._meta.get_fields():
                if isinstance(field, ForeignKey):
                    copy_models_to_postgres(field.related_model)

            print "importing %s" % repr(model)
            model.objects.using('postgres').delete()

            if ((model not in [Page, PageRevision, CFGOVAuthoredPages])
                    and not issubclass(model, (Page, TaggedItemBase))):
                qs = model.objects.using('default').all().iterator()
                if model._meta.parents:
                    slow_save(*qs)
                else:
                    model.objects.using('postgres').bulk_create(qs, batch_size=100)

            elif issubclass(model,Page):
                for obj in model.objects.using('default').all():

                    #if isinstance(obj, CFGOVTaggedPages):
                    #    try:
                    #        obj.content_object
                    #    except Page.DoesNotExist:
                    #        continue
                    #if isinstance(obj, Answer):
                    #    extra_save_options['skip_page_update'] = True


                    #if isinstance(obj, Page):
                    # numchild numbers seem to screw with the save
                    # so let's just zero them out
                    obj.numchild = 0

                    try:
                        slow_save(obj)
                    except ValidationError as e:
                        # there are some pages in the Trash with
                        # duplicate slugs (somehow)
                        # we'll "fix" the slug and try again
                        if 'slug' in e.error_dict:
                            obj.slug = obj.slug + str(obj.pk)
                            slow_save(obj)
                            continue
                        else:
                            raise
                    if model is Page:
                        # for some reason, this proved more reliable than
                        # importing all of the revisions at once
                        revisions = obj.revisions.all().iterator()
                        PageRevision.objects.using('postgres').bulk_create(
                            revisions)

            elif issubclass(model, TaggedItemBase):
                for obj in model.objects.using('default').all():
                    try:
                        # some of these no longer point to a valid page
                        # so skip them
                        obj.content_object
                        slow_save(obj)
                    except Page.DoesNotExist:
                        continue


            # import any "through" models
            for m2mfield in model._meta.many_to_many:
                m2m_model = getattr(model, m2mfield.name).through
                copy_models_to_postgres(m2m_model)


def run():
    # Even with --no-initial-data, there's still some tables we need
    # to zap before we can start populating the DB
    # This also helps with overwriting previous imports
    # SEEN_MODELS.append(CFGOVAuthoredPages)
    SEEN_MODELS.append(PageRevision)
    SEEN_MODELS.append(Revision)
    SEEN_MODELS.append(Version)
    obliterate('ask_cfpb_answerlandingpage',
               'v1_landingpage',
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
               'v1_cfgovauthoredpages',
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

    all_models = apps.get_models(include_auto_created=True)
    copy_models_to_postgres(*all_models)
