# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0078_auto_20160419_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legacyblogpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'content', wagtail.wagtailcore.blocks.RawHTMLBlock(help_text=b'Content from WordPress unescaped.'))]),
        ),
    ]
