# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps as imported_apps
from django.db import migrations, transaction

from v1.tests.wagtail_pages.helpers import (
    get_page_stream_data, set_page_stream_data
)


def migrate_hero_forwards(data):
    data = dict(data)

    data['small_image'] = data['image']['upload']
    data['image'] = data.pop('background_image', None)

    return data


def migrate_hero_backwards(data):
    data = dict(data)

    data['background_image'] = data['image']

    small_image = data.pop('small_image', None)
    if small_image:
        data['image'] = {'upload': small_image, 'alt': ''}

    return data


def migrate_page(page, field_name, mapper):
    old_stream_data = get_page_stream_data(page, field_name)
    new_stream_data = []

    migrated = False
    for field in old_stream_data:
        if 'hero' == field['type']:
            field['value'] = mapper(field['value'])
            migrated = True

        new_stream_data.append(field)

    if migrated:
        print('migrated page {}'.format(page.slug))
        set_page_stream_data(page, field_name, new_stream_data)


@transaction.atomic
def migrate_heroes(apps, mapper):
    page_types_and_stream_fields_with_heroes = [
        ('DemoPage', 'molecules'),
        ('LandingPage', 'header'),
        ('SublandingFilterablePage', 'header'),
        ('SublandingPage', 'header'),
    ]

    for page_type, field_name in page_types_and_stream_fields_with_heroes:
        page_cls = imported_apps.get_model('v1', page_type)
        for page in page_cls.objects.all():
            migrate_page(page, field_name, mapper)


def forwards(apps, schema_editor):
    migrate_heroes(apps, migrate_hero_forwards)


def backwards(apps, schema_editor):
    migrate_heroes(apps, migrate_hero_backwards)


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v1', '0010_hero_refactor'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
