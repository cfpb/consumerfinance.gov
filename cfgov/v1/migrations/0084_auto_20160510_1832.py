# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0083_auto_20160504_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'full_width_text', wagtail.wagtailcore.blocks.StreamBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(icon=b'edit')), (b'media', wagtail.wagtailimages.blocks.ImageChooserBlock(icon=b'image')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'body', wagtail.wagtailcore.blocks.TextBlock()), (b'citation', wagtail.wagtailcore.blocks.TextBlock())])), (b'cta', wagtail.wagtailcore.blocks.StructBlock([(b'slug_text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph_text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'button', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))])), (b'related_links', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])))])), (b'table', wagtail.wagtailcore.blocks.StructBlock([(b'headers', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock())), (b'rows', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StreamBlock([(b'hyperlink', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'text', wagtail.wagtailcore.blocks.CharBlock()), (b'text_blob', wagtail.wagtailcore.blocks.TextBlock()), (b'rich_text_blob', wagtail.wagtailcore.blocks.RichTextBlock())])))]))])), (b'image_text_50_50_group', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False, icon=b'title')), (b'image_texts', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False, blank=True)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'is_widescreen', wagtail.wagtailcore.blocks.BooleanBlock(required=False, label=b'Use 16:9 image')), (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(required=False, label=b'Show links as button')), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))])))]))]),
        ),
    ]
