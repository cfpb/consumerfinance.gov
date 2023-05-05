import copy
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from wagtail.blocks import StreamValue

from treebeard.mp_tree import MP_Node


def get_page(page_cls, slug):
    return page_cls.objects.get(slug=slug)


def get_free_path(apps, parent_page):
    offset = 1
    base_page_cls = apps.get_model("wagtailcore", "Page")

    while True:
        path = MP_Node._get_path(
            parent_page.path,
            parent_page.depth + 1,
            parent_page.numchild + offset,
        )

        try:
            base_page_cls.objects.get(path=path)
        except base_page_cls.DoesNotExist:
            return path

        offset += 1


@transaction.atomic
def get_or_create_page(
    apps,
    page_cls_app,
    page_cls_name,
    title,
    slug,
    parent_page,
    live=False,
    **kwargs,
):
    page_cls = apps.get_model(page_cls_app, page_cls_name)

    try:
        return get_page(page_cls, slug)
    except ObjectDoesNotExist:
        pass

    ContentType = apps.get_model("contenttypes.ContentType")

    page_content_type = ContentType.objects.get_for_model(page_cls)

    parent_page = get_page(parent_page.specific_class, parent_page.slug)

    page = page_cls.objects.create(
        title=title,
        slug=slug,
        depth=parent_page.depth + 1,
        path=get_free_path(apps, parent_page),
        content_type=page_content_type,
        live=live,
        **kwargs,
    )

    parent_page.numchild += 1
    parent_page.save()

    return page


def is_page(page_or_revision):
    """Return True if the page_or_revision is a Page object"""
    return hasattr(page_or_revision, "live_revision")


def get_streamfield_data(page_or_revision, field_name):
    """Get the streamfield data for a given field name on a page or a
    revision"""
    if is_page(page_or_revision):
        field = getattr(page_or_revision, field_name)
        return field.raw_data
    else:
        field = page_or_revision.content.get(field_name, "[]")
        return json.loads(field)


def set_streamfield_data(page_or_revision, field_name, data, commit=True):
    """Set the streamfield data for a given field name on a page or a
    revision. If commit is True (default) save() is called on the
    page_or_revision object."""
    if is_page(page_or_revision):
        field = getattr(page_or_revision, field_name)
        stream_block = field.stream_block
        stream_value = StreamValue(stream_block, data, is_lazy=True)
        setattr(page_or_revision, field_name, stream_value)
    else:
        page_or_revision.content[field_name] = json.dumps(data)

    if commit:
        page_or_revision.save()


def _is_listblock(value):
    return isinstance(value, list) and not any(
        "type" in block and "value" in block for block in value
    )


def migrate_block(page_or_revision, child_block_path, block_value, mapper):
    is_listblock = _is_listblock(block_value)

    if not child_block_path and not is_listblock:
        original_value = copy.deepcopy(block_value)
        mapped_value = mapper(page_or_revision, block_value)
        return mapped_value, (original_value != mapped_value)

    if is_listblock:
        migrator = migrate_listblock
    elif isinstance(block_value, list):
        migrator = migrate_streamblock
    elif isinstance(block_value, dict):
        migrator = migrate_structblock
    else:
        raise ValueError("unexpected block value: %s" % block_value)

    return migrator(page_or_revision, child_block_path, block_value, mapper)


def migrate_streamblock(page_or_revision, block_path, block, mapper):
    migrated = False
    child_block_name, remaining_block_path = block_path[0], block_path[1:]

    for child_block in block:
        if child_block["type"] != child_block_name:
            continue

        migrated_value, child_migrated = migrate_block(
            page_or_revision,
            remaining_block_path,
            child_block["value"],
            mapper,
        )

        if child_migrated:
            child_block["value"] = migrated_value
            migrated = True

    return block, migrated


def migrate_structblock(page_or_revision, block_path, block, mapper):
    migrated = False
    child_block_name, remaining_block_path = block_path[0], block_path[1:]

    child_block = block.get(child_block_name)

    if child_block:
        migrated_value, child_migrated = migrate_block(
            page_or_revision, remaining_block_path, child_block, mapper
        )

        if child_migrated:
            block[child_block_name] = migrated_value
            migrated = True

    return block, migrated


def migrate_listblock(page_or_revision, block_path, block, mapper):
    migrated = False

    for i in range(len(block)):
        child_block = block[i]

        migrated_value, child_migrated = migrate_block(
            page_or_revision, block_path, child_block, mapper
        )

        if child_migrated:
            block[i] = migrated_value
            migrated = True

    return block, migrated


def migrate_streamfield_data(page_or_revision, block_path, data, mapper):
    if not block_path:
        return data, False

    if isinstance(block_path, str):
        block_path = [
            block_path,
        ]
    elif isinstance(block_path, tuple):
        block_path = list(block_path)

    return migrate_streamblock(page_or_revision, block_path, data, mapper)


def migrate_stream_field(page_or_revision, field_name, block_path, mapper):
    """Run mapper on blocks within a StreamField on a page or revision."""
    data = get_streamfield_data(page_or_revision, field_name)

    data, migrated = migrate_streamfield_data(
        page_or_revision, block_path, data, mapper
    )

    if migrated:
        set_streamfield_data(page_or_revision, field_name, data)


@transaction.atomic
def migrate_page_types_and_fields(apps, page_types_and_fields, mapper):
    """Migrate Wagtail StreamFields using the given mapper function.
    page_types_and_fields should be a list of 4-tuples
    providing ('app', 'PageType', 'field_name', ('block_path', )).
    'field_name' is the field on the 'PageType' model.
    'block path' is a tuple containing block names to access the
    StreamBlock type to migrate."""
    for app, page_type, field_name, block_path in page_types_and_fields:
        page_model = apps.get_model(app, page_type)

        # We need to support both the pre-Wagtail 4 "PageRevision" model as
        # well as the post-Wagtail 4 "Revision" model, because some of our
        # data migrations run before Wagtail 4's migration from PageRevision
        # to Revision.
        # TODO: When we squash migrations replace this test with *just*
        # "wagtailcore.Revision". Any of those migrations should already be
        # applied to our database dumps, and it should be a noop on new
        # database initialization.
        try:
            revision_model = apps.get_model("wagtailcore.Revision")
        except LookupError:  # pragma: no cover
            revision_model = apps.get_model("wagtailcore.PageRevision")

        for page in page_model.objects.all():
            migrate_stream_field(page, field_name, block_path, mapper)

            revisions = revision_model.page_revisions.filter(
                object_id=page.id
            ).order_by("-id")
            for revision in revisions:
                migrate_stream_field(revision, field_name, block_path, mapper)


# This is a temporary function that is used in the following migrations:
#   v1.migrations.0210_convert_email_signup_blocks.
#
# Once that migration is complete, those migrations should be converted to
# noops and this function can be deleted.
def convert_emailsignup_block_to_snippet(apps, page_or_revision, data):
    # Get the models we need
    EmailSignUp = apps.get_model("v1", "EmailSignUp")
    Page = apps.get_model("wagtailcore", "Page")

    # Get or create a snippet for the EmailSignUpBlock data we received.
    emailsignup_snippet, created = EmailSignUp.objects.get_or_create(
        heading=data["heading"],
        default_heading=data.get("default_heading", True),
        text=data["text"],
        code=data["gd_code"],
        disclaimer_page=(
            Page.objects.get(pk=data["disclaimer_page"])
            if data["disclaimer_page"] is not None
            else None
        ),
    )

    # Return the primary key of that snippet object
    return emailsignup_snippet.pk
