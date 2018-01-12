import re
from StringIO import StringIO

from django.apps import apps
from django.db import connections
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.core import management
from django.db.models.fields.related import ForeignKey

from taggit.models import TaggedItemBase
from wagtail.wagtailcore.models import Page, PageRevision

from reversion.models import Revision, Version

from v1.models.base import CFGOVAuthoredPages

SEEN_MODELS = []
ALREADY_OBLITERATED = []


def slow_save(*objects):
    for obj in objects:
        obj.save(using='postgres')


def obliterate(*table_names):
    pg_cursor = connections['postgres'].cursor()
    for table_name in table_names:
        if table_name in ALREADY_OBLITERATED:
            continue
        try:
            pg_cursor.execute('delete from %s' % table_name)
            ALREADY_OBLITERATED.append(table_name)
        except IntegrityError as exception:
            # extract the problematic table from the exception text
            # A regex would work too.
            problematic_table = exception.message.split('"')[-2]
            obliterate(problematic_table)
            obliterate(table_name)


def copy_models_to_postgres(*models):
    for model in models:

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
            obliterate(model._meta.db_table)
            # Use bulk_create, except where problematic or impossible
            
            if ((model not in [Page, PageRevision, CFGOVAuthoredPages])
                    and not issubclass(model, (Page, TaggedItemBase))):
                qs = model.objects.using('default').all().iterator()
                if model._meta.parents:
                    slow_save(*qs)
                else:
                    model.objects.using('postgres').bulk_create(
                        qs, batch_size=100)

            elif issubclass(model,Page):
                for obj in model.objects.using('default').all():

                    # numchild numbers seem to screw with the save
                    # so let's just zero them out
                    # this means we need to run Wagtail's 'fixtree'
                    obj.numchild = 0

                    try:
                        slow_save(obj)
                    except ValidationError as exception:
                        # there are some pages in the Trash with
                        # duplicate slugs (somehow)
                        # we'll "fix" the slug and try again
                        if 'slug' in exception.error_dict:
                            obj.slug = obj.slug + str(obj.pk)
                            slow_save(obj)
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

    all_models = apps.get_models(include_auto_created=True)
    copy_models_to_postgres(*all_models)

    # update auto-incrementing sequences:
    # https://stackoverflow.com/a/44113124

    app_labels = [a.label for a in apps.get_app_configs()]
    sql_captured = StringIO()

    management.call_command('sqlsequencereset',
                            *app_labels, stdout=sql_captured,
                            database='postgres')

    sql = sql_captured.getvalue()

    # Remove terminal color codes from sqlsequencereset output
    ansi_escape = re.compile(r'\x1b[^m]*m')
    sql = ansi_escape.sub('', sql)

    cursor = connections['postgres'].cursor()
    cursor.execute(sql)
