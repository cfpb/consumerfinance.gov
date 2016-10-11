# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from v1.util.migrations import migrate_page_types_and_fields


def migrate_category_field_forwards(page, data):
    data = dict(data)

    # If the original category field is empty, we take that to mean
    # show_category should be False.
    if data['category'] == '':
        data['show_category'] = False
    else:
        data['show_category'] = True

    del data['category']

    return data


def migrate_category_field_backwards(page, data):
    data = dict(data)

    # If show_category is true, we need to get the first category from
    # the page settings categories and assign its name to the categories
    # field.
    if data['show_category'] is True and \
            len(page.categories.values) > 0:
        data['category'] = page.categories.values[0]['name']
    else:
        data['category'] = ''

    del data['show_category']
    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('AbstractFilterPage', 'header', 'item_introduction'),
        ('DemoPage', 'header', 'item_introduction'),
    ]
    migrate_page_types_and_fields(apps, page_types_and_fields,
                                  migrate_category_field_forwards)


def backwards(apps, schema_editor):
    page_types_and_fields = [
        ('AbstractFilterPage', 'header', 'item_introduction'),
        ('DemoPage', 'header', 'item_introduction'),
    ]
    migrate_page_types_and_fields(apps, page_types_and_fields,
                                  migrate_category_field_backwards)


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0020_replace_dup_category_field'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
