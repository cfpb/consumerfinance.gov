# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0114_update_menu_item_link_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='nav_footer',
            field=wagtail.wagtailcore.fields.StreamField([(b'nav_footer', wagtail.wagtailcore.blocks.StructBlock([(b'draft', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'If checked, this block will only show on our sharing site (Content).', default=False, required=False, label=b'Mark block as draft')), (b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=False, features=[b'link']))], label=b'Menu footer'))], blank=True),
        ),
    ]
