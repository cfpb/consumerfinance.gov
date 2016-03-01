# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


def migrate_text_intro_blocks(apps, schema_editor):
    SublandingPage = apps.get_model('v1.SublandingPage')

    for page in SublandingPage.objects.all():
        for i, child in enumerate(page.header.stream_data):
            if child['type'] == 'text_introduction':
                page.content.stream_data = [child] + page.content.stream_data
                del page.header.stream_data[i]
                page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0053_homepage'),
    ]

    operations = [
        migrations.RunPython(migrate_text_intro_blocks),
        migrations.AlterField(
            model_name='sublandingpage',
            name='header',
            field=wagtail.wagtailcore.fields.StreamField([(b'hero', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'background_color', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Use Hexcode colors e.g #F0F8FF', required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))), (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(required=False))]))], blank=True),
        ),
    ]
