import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from treebeard.mp_tree import MP_Node


try:
    from wagtail.core.blocks import StreamValue
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.blocks import StreamValue


def get_page(page_cls, slug):
    return page_cls.objects.get(slug=slug)


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
                       parent_page, live=False, **kwargs):
    page_cls = apps.get_model(page_cls_app, page_cls_name)

    try:
        return get_page(page_cls, slug)
    except ObjectDoesNotExist:
        pass

    ContentType = apps.get_model('contenttypes.ContentType')

    page_content_type = ContentType.objects.get_for_model(page_cls)

    parent_page = get_page(parent_page.specific_class, parent_page.slug)

    page = page_cls.objects.create(
        title=title,
        slug=slug,
        depth=parent_page.depth + 1,
        path=get_free_path(apps, parent_page),
        content_type=page_content_type,
        live=live,
        **kwargs
    )

    parent_page.numchild += 1
    parent_page.save()

    return page


def is_page(page_or_revision):
    """ Return True if the page_or_revision is a Page object """
    return not hasattr(page_or_revision, 'content_json')


def get_stream_data(page_or_revision, field_name):
    """ Get the stream field data for a given field name on a page or a
    revision """
    if is_page(page_or_revision):
        field = getattr(page_or_revision, field_name)
        return field.stream_data
    else:
        revision_content = json.loads(page_or_revision.content_json)
        field = revision_content.get(field_name, "[]")
        return json.loads(field)


def set_stream_data(page_or_revision, field_name, stream_data, commit=True):
    """ Set the stream field data for a given field name on a page or a
    revision. If commit is True (default) save() is called on the
    page_or_revision object. """
    if is_page(page_or_revision):
        field = getattr(page_or_revision, field_name)
        stream_block = field.stream_block
        stream_value = StreamValue(stream_block, stream_data, is_lazy=True)
        setattr(page_or_revision, field_name, stream_value)
    else:
        revision_content = json.loads(page_or_revision.content_json)
        revision_content[field_name] = json.dumps(stream_data)
        page_or_revision.content_json = json.dumps(revision_content)

    if commit:
        page_or_revision.save()


def migrate_stream_data(page_or_revision, block_path, stream_data, mapper):
    """ Recursively run the mapper on fields of block_type in stream_data """
    migrated = False

    if isinstance(block_path, str):
        block_path = [block_path, ]

    if len(block_path) == 0:
        return stream_data, False

    # Separate out the current block name from its child paths
    block_name = block_path[0]
    child_block_path = block_path[1:]

    for field in stream_data:
        if field['type'] == block_name:
            if len(child_block_path) == 0:
                value = mapper(page_or_revision, field['value'])
                field_migrated = True
            else:
                value, field_migrated = migrate_stream_data(
                    page_or_revision, child_block_path, field['value'], mapper
                )

            if field_migrated:
                field['value'] = value
                migrated = True

    return stream_data, migrated


def migrate_stream_field(page_or_revision, field_name, block_path, mapper):
    """ Run mapper on blocks within a StreamField on a page or revision. """
    stream_data = get_stream_data(page_or_revision, field_name)

    stream_data, migrated = migrate_stream_data(
        page_or_revision, block_path, stream_data, mapper
    )

    if migrated:
        set_stream_data(page_or_revision, field_name, stream_data)


@transaction.atomic
def migrate_page_types_and_fields(apps, page_types_and_fields, mapper):
    """ Migrate Wagtail StreamFields using the given mapper function.
        page_types_and_fields should be a list of 4-tuples
        providing ('app', 'PageType', 'field_name', ('block_path', )).
        'field_name' is the field on the 'PageType' model.
        'block path' is a tuple containing block names to access the
        StreamBlock type to migrate."""
    for app, page_type, field_name, block_path in page_types_and_fields:
        page_model = apps.get_model(app, page_type)
        revision_model = apps.get_model('wagtailcore.PageRevision')

        for page in page_model.objects.all():
            migrate_stream_field(page, field_name, block_path, mapper)

            revisions = revision_model.objects.filter(
                page=page).order_by('-id')
            for revision in revisions:
                migrate_stream_field(revision, field_name, block_path, mapper)
