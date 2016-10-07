from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from treebeard.mp_tree import MP_Node

from django.apps import apps as imported_apps
from v1.tests.wagtail_pages.helpers import (
    get_page_stream_data, set_page_stream_data)


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


def migrate_stream_field(page, field_name, field_type, mapper):
    """ Migrate a stream field of the name and type belonging to
        the page using the mapper function """
    old_stream_data = get_page_stream_data(page, field_name)
    new_stream_data = []

    migrated = False
    for field in old_stream_data:
        if field_type == field['type']:
            field['value'] = mapper(page, field['value'])
            migrated = True

        new_stream_data.append(field)

    if migrated:
        print('migrated page {}'.format(page.slug))
        set_page_stream_data(page, field_name, new_stream_data)


@transaction.atomic
def migrate_page_types_and_fields(apps, page_types_and_fields, mapper):
    for page_type, field_name, field_type in page_types_and_fields:
        page_cls = imported_apps.get_model('v1', page_type)
        for page in page_cls.objects.all():
            migrate_stream_field(page, field_name, field_type, mapper)
