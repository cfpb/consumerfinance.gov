# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailsnippets.blocks
import v1.models.snippets
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0013_add_sublanding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sublandingpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(icon=b'title')), (b'image_text_25_75', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=True)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False))])), (b'image_text_50_50_group', wagtail.wagtailcore.blocks.StructBlock([(b'image_texts', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))])), (b'is_widescreen', wagtail.wagtailcore.blocks.BooleanBlock(required=False, label=b'Use 16:9 image')), (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(required=False, label=b'Show links as button')), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))])))])), (b'full_width_text', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=True))])), (b'half_width_link_blob_group', wagtail.wagtailcore.blocks.StructBlock([(b'link_blobs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))])))])), (b'well', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=True, label=b'Well'))])), (b'table', wagtail.wagtailcore.blocks.StructBlock([(b'headers', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock(max_length=20))), (b'rows', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StreamBlock([(b'hyperlink', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=20)), (b'text_blob', wagtail.wagtailcore.blocks.TextBlock()), (b'rich_text_blob', wagtail.wagtailcore.blocks.RichTextBlock())])))])), (b'contact', wagtail.wagtailcore.blocks.StructBlock([(b'header', wagtail.wagtailcore.blocks.CharBlock()), (b'body', wagtail.wagtailcore.blocks.RichTextBlock()), (b'contact', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(v1.models.snippets.Contact))]))], blank=True),
        ),
    ]
