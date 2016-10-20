# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations

from wagtail.wagtailcore.models import Page, PageRevision

from v1.util.migrations import migrate_page_types_and_fields, is_page


def migrate_category_field_forwards(page_or_revision, data):
    data = dict(data)

    # If the original category field is empty, we take that to mean
    # show_category should be False.
    data['show_category'] = bool(data.pop('category', None))

    return data


def migrate_category_field_backwards(page_or_revision, data):
    data = dict(data)

    # If show_category is true, we need to get the first category from
    # the page settings categories and assign its name to the categories
    # field.
    if data.pop('show_category'):
        if is_page(page_or_revision):
            categories = page_or_revision.categories
        else:
            revision_content = json.loads(page_or_revision.content_json)
            categories = revision_content['categories']

        try:
            data['category'] = categories[0]['name']
        except IndexError:
            # If the page or revision doesn't have any categories, we'll get an
            # IndexError
            data['category'] = ''
    else:
        data['category'] = ''

    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('v1', 'DocumentDetailPage', 'header', 'item_introduction'),
        ('v1', 'LearnPage', 'header', 'item_introduction'),
        ('v1', 'EventPage', 'header', 'item_introduction'),
        ('v1', 'DemoPage', 'header', 'item_introduction'),
    ]
    migrate_page_types_and_fields(apps, page_types_and_fields,
                                  migrate_category_field_forwards)


def backwards(apps, schema_editor):
    page_types_and_fields = [
        ('v1', 'AbstractFilterPage', 'header', 'item_introduction'),
        ('v1', 'DemoPage', 'header', 'item_introduction'),
    ]
    migrate_page_types_and_fields(apps, page_types_and_fields,
                                  migrate_category_field_backwards)


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0021_replace_dup_category_field'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
