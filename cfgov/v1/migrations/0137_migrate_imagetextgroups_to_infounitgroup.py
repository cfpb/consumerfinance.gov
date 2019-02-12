""" This data migration converts Image & Text Groups to Info Unit Groups.

The ImageText5050Group and ImageText2575Group organisms have this format:

{
    # string, not required
    'heading': 'Heading',

    # boolean, not required, defaults to False
    'link_image_and_heading': True,

    # StructBlock, ImageText5050Group only
    'sharing': {
        # boolean, not required, defaults to False
        'shareable': False

        # string, not required
        'share_blurb': 'Tweet text, e-mail subject line, and LinkedIn post'
    },

    # ListBlock of ImageText5050 or ImageText2575 molecules
    'image_texts': [
        {
            # string, not required
            'heading': 'Heading',

            # rich text, not required
            'body': '<p>HTML text</p>',

            # ImageBasic atom
            'image': <ImageBasic PK>,

            # ListBlock of Hyperlink atoms
            'links': [
                {
                    'text': 'Link text'
                    'url': '/path/to/something/'
                },
                ...
            ]

            # boolean, not required, defaults to False, ImageText2575 only
            has_rule: False,

            # boolean, not required, defaults to False, ImageText5050 only
            is_widescreen: False,

            # boolean, not required, defaults to False, ImageText5050 only
            is_button: False,
        },
        ...
    ]
}


The InfoUnitGroup organism has the following format:

{
    # ChoiceBlock; choices of '50-50', '25-75', or '33-33-33'; required
    format: '50-50',

    # HeadingBlock
    'heading': {
        # string, not required
        'text': 'Heading',

        # ChoiceBlock; choices of 'h2', 'h3', or 'h4'; not required
        'level': 'h2'

        # string, not required
        'icon': 'help-round'
    },

    # rich text, not required
    'intro': '<p>HTML text</p>',

    # boolean, not required, defaults to True
    'link_image_and_heading': True,

    # boolean, not required, defaults to False
    'has_top_rule_line': False,

    # boolean, not required, defaults to False
    'lines_between_items': False,

    # ListBlock of InfoUnit molecules
    'info_units': [
        {
            # ImageBasic atom
            'image': <ImageBasic PK>,

            # HeadingBlock
            'heading': {
                # string, not required
                'text': 'Heading',

                # ChoiceBlock; choices of 'h2', 'h3', or 'h4'; not required
                'level': 'h3'

                # string, not required
                'icon': 'help-round'
            },

            # rich text, not required
            'body': '<p>HTML text</p>',

            # ListBlock of Hyperlink atoms
            'links': [
                {
                    'text': 'Link text'
                    'url': '/path/to/something/'
                },
                ...
            ]
        },
        ...
    ],

    # StructBlock
    'sharing': {
        # boolean, not required, defaults to False
        'shareable': False

        # string, not required
        'share_blurb': 'Tweet text, e-mail subject line, and LinkedIn post'
    }
}
"""


from django.db import migrations

from v1.util.migrations import get_stream_data, set_stream_data


def image_text_group_to_info_unit_group(old_value, new_format):
    new_value = {}

    # Convert basic heading CharBlock to HeadingBlock.
    if old_value.get('heading'):
        new_value['heading'] = {
            'text': old_value['heading'],
            'level': 'h2',
        }

    # If any image_texts are defined, process those.
    if old_value.get('image_texts'):
        image_texts = old_value['image_texts']
        info_units = []

        for image_text in image_texts:
            info_unit = {}

            # Convert basic heading CharBlock to HeadingBlock.
            if image_text.get('heading'):
                info_unit['heading'] = {
                    'text': image_text['heading'],
                    'level': 'h3',
                }

            # If at least one image_text has checked has_rule,
            # assume we want them between all
            if image_text.get('has_rule'):
                new_value['lines_between_items'] = True

            # Fields that need no manipulation: body, image, links.
            if image_text.get('body'):
                info_unit['body'] = image_text['body']
            if image_text.get('image'):
                info_unit['image'] = image_text['image']
            if image_text.get('links'):
                info_unit['links'] = image_text['links']
            else:
                info_unit['links'] = []

            # Fields being discarded: is_widescreen, is_button.

            # If at least one field was copied, append new info_unit to list.
            if info_unit:
                info_units.append(info_unit)

        new_value['info_units'] = info_units

    # The one field that needs no manipulation: sharing.
    if old_value.get('sharing'):
        new_value['sharing'] = old_value['sharing']

    # This one has to be more explicit because it now defaults to True,
    # but we don't want it to be True if it wasn't set before.
    if old_value.get('link_image_and_heading'):
        new_value['link_image_and_heading'] = True
    else:
        new_value['link_image_and_heading'] = False

    # Add new required field: format.
    new_value['format'] = new_format

    return new_value


def migrate_streamfield_forward(page_or_revision, streamfield_name, new_type):
    """ Migrate a StreamField belonging to the page or revision """
    old_stream_data = get_stream_data(page_or_revision, streamfield_name)

    new_stream_data = []
    migrated = False

    block_conversions = {
        'image_text_25_75_group': '25-75',
        'image_text_50_50_group': '50-50',
    }

    for block in old_stream_data:
        block_type = block['type']

        if block_type in block_conversions:
            new_block = {
                'type': new_type,
                'value': image_text_group_to_info_unit_group(
                    block['value'],
                    block_conversions[block_type]
                )
            }

            new_stream_data.append(new_block)
            migrated = True
        else:
            new_stream_data.append(block)

    if migrated:
        set_stream_data(
            page_or_revision,
            streamfield_name,
            new_stream_data
        )


def forwards(apps, schema_editor):
    models_and_fields = [
        ('v1', 'BlogPage', 'content'),
        ('v1', 'BrowsePage', 'content'),
        ('v1', 'LandingPage', 'content'),
        ('v1', 'LearnPage', 'content'),
        ('v1', 'SublandingPage', 'content'),
    ]

    revision_model = apps.get_model('wagtailcore.PageRevision')

    for app, page_type, streamfield_name in models_and_fields:
        page_model = apps.get_model(app, page_type)
        if page_type == 'LearnPage':
            new_type = 'info_unit_group_25_75_only'
        else:
            new_type = 'info_unit_group'

        for page in page_model.objects.all():
            migrate_streamfield_forward(page, streamfield_name, new_type)

            # Migrate revisions
            revisions = revision_model.objects.filter(
                page=page).order_by('-id')
            for revision in revisions:
                migrate_streamfield_forward(
                    revision,
                    streamfield_name,
                    new_type
                )


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0136_remove_htmlblock_from_browsepage'),
    ]

    operations = [
         migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
