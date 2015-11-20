# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0014_auto_20151120_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='half_width_link_blob_content',
            field=wagtail.wagtailcore.fields.StreamField([(b'half_width_link_blob', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))]))], verbose_name=b'content', blank=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='half_width_link_blob_group_header',
            field=models.CharField(max_length=100, verbose_name=b'Group Header', blank=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='image_text_25_75_content',
            field=wagtail.wagtailcore.fields.StreamField([(b'image_text_25_75', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=True)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False))]))], verbose_name=b'content', blank=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='image_text_25_75_group_header',
            field=models.CharField(max_length=100, verbose_name=b'Group Header', blank=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='image_text_50_50_content',
            field=wagtail.wagtailcore.fields.StreamField([(b'image_text_50_50', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))])), (b'is_widescreen', wagtail.wagtailcore.blocks.BooleanBlock(required=False, label=b'Use 16:9 image')), (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(required=False, label=b'Show links as button')), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))]))], verbose_name=b'content', blank=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='image_text_50_50_group_header',
            field=models.CharField(max_length=100, verbose_name=b'Group Header', blank=True),
        ),
    ]
