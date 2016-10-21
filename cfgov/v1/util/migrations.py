from __future__ import print_function

import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from wagtail.wagtailcore.blocks import StreamValue
from treebeard.mp_tree import MP_Node


def get_page(apps, slug):
    base_page_cls = apps.get_model('wagtailcore', 'Page')
    return base_page_cls.objects.get(slug=slug)


def get_free_path(apps, parent_page):
    offset = 1
    base_page_cls = apps.get_model('wagtailcore', 'Page')

    while True:
        path = MP_Node._get_path(
            parent_page.path,
            parent_page.depth + 1,
            parent_page.numchild + offset
        )

        try:
            base_page_cls.objects.get(path=path)
        except base_page_cls.DoesNotExist:
            return path

        offset += 1


@transaction.atomic
def get_or_create_page(apps, page_cls_app, page_cls_name, title, slug,
                       parent_page, live=False, shared=False, **kwargs):
    try:
        return get_page(apps, slug)
    except ObjectDoesNotExist:
        pass

    ContentType = apps.get_model('contenttypes.ContentType')
    page_cls = apps.get_model(page_cls_app, page_cls_name)

    page_content_type = ContentType.objects.get_for_model(page_cls)

    parent_page = get_page(apps, slug=parent_page.slug)

    page = page_cls.objects.create(
        title=title,
        slug=slug,
        depth=parent_page.depth + 1,
        path=get_free_path(apps, parent_page),
        content_type=page_content_type,
        live=live,
        shared=shared,
        **kwargs
    )

    parent_page.numchild += 1
    parent_page.save()

    return page


def get_stream_data(page_or_revision, field_name):
    """ Get the stream field data for a given field name on a page or a
    revision """
    try:
        # If page_or_revision is a page, this will work
        field = getattr(page_or_revision, field_name)
        stream_data = field.stream_data
    except AttributeError:
        # Otherwise it will raise an Attribute error and we can assume
        # page_or_revision is a revision
        revision_content = json.loads(page_or_revision.content_json)
        field = revision_content[field_name]
        stream_data = json.loads(field)
    return stream_data


def set_stream_data(page_or_revision, field_name, stream_data):
    """ Set the stream field data for a given field name on a page or a
    revision """
    try:
        # If page_or_revision is a page, this will work
        field = getattr(page_or_revision, field_name)
        stream_block = field.stream_block
        stream_value = StreamValue(stream_block, stream_data, is_lazy=True)
        setattr(page_or_revision, field_name, stream_value)
        page_or_revision.save()
    except AttributeError:
        # Otherwise it will raise an Attribute error and we can assume
        # page_or_revision is a revision
        revision_content = json.loads(page_or_revision.content_json)
        revision_content[field_name] = json.dumps(stream_data)
        page_or_revision.content_json = json.dumps(revision_content)
        page_or_revision.save()


def migrate_stream_field(page_or_revision, field_name, field_type, mapper):
    """ Migrate a stream field of the name and type belonging to
        the page using the mapper function """
    old_stream_data = get_stream_data(page_or_revision, field_name)
    new_stream_data = []

    migrated = False
    for field in old_stream_data:
        if field_type == field['type']:
            field['value'] = mapper(page_or_revision, field['value'])
            migrated = True

        new_stream_data.append(field)

    if migrated:
        print('migrated page {}'.format(page_or_revision))
        set_stream_data(page_or_revision, field_name, new_stream_data)


@transaction.atomic
def migrate_page_types_and_fields(apps, page_types_and_fields, mapper):
    """ Migrate the fields of a wagtail page type using the given mapper
        function. page_types_and_fields should be a list of 3-tuples
        providing ('PageType', 'field_name', 'field type'). """
    for page_type, field_name, field_type in page_types_and_fields:
        page_model = apps.get_model('v1', page_type)
        revision_model = apps.get_model('wagtailcore.PageRevision')
        for page in page_model.objects.all():
            migrate_stream_field(page, field_name, field_type, mapper)

            revisions = revision_model.objects.filter(
                page=page).order_by('-id')
            for revision in revisions:
                migrate_stream_field(revision, field_name, field_type, mapper)
