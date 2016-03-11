# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0061_auto_20160311_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='header',
            field=wagtail.wagtailcore.fields.StreamField([(b'half_width_link_blob', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False, blank=True)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))]))], blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='latest_updates',
            field=wagtail.wagtailcore.fields.StreamField([(b'posts', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'categories', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'speech-bubble', b'Blog'), (b'newspaper', b'Newsroom'), (b'document', b'Report'), (b'date', b'Events'), (b'microphone', b'Speech'), (b'bullhorn', b'Press Release'), (b'contract', b'Op-Ed'), (b'double-quote', b'Testimony')])), (b'link', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'date', wagtail.wagtailcore.blocks.DateTimeBlock(required=False)), (b'render_all_activities_link', wagtail.wagtailcore.blocks.BooleanBlock(required=False))])))], blank=True),
        ),
    ]
