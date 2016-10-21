# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps as imported_apps
from django.db import migrations, transaction

from v1.util.migrations import (
    get_stream_data, set_stream_data
)


def migrate_hero_forwards(data):
    data = dict(data)

    image = (data.get('image') or {}).get('upload')
    background_image = data.pop('background_image', None)

    if background_image:
        data['small_image'] = image
        data['image'] = background_image
    else:
        data['small_image'] = None
        data['image'] = image

    return data


def migrate_hero_backwards(data):
    data = dict(data)

    image = data['image']
    small_image = data.pop('small_image', None)

    data['image'] = None
    data['background_image'] = None

    if image and small_image:
        data['image'] = {'upload': small_image, 'alt': ''}
        data['background_image'] = image
    elif image:
        data['image'] = {'upload': image, 'alt': ''}
    elif small_image:
        data['image'] = {'upload': small_image, 'alt': ''}

    return data


def migrate_page(page, field_name, mapper):
    old_stream_data = get_stream_data(page, field_name)
    new_stream_data = []

    migrated = False
    for field in old_stream_data:
        if 'hero' == field['type']:
            field['value'] = mapper(field['value'])
            migrated = True

        new_stream_data.append(field)

    if migrated:
        print('migrated page {}'.format(page.slug))
        set_stream_data(page, field_name, new_stream_data)


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
