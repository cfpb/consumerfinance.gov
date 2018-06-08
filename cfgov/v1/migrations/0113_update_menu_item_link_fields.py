# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0112_add_menu_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='external_link',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='page_link',
            field=models.ForeignKey(related_name='+', blank=True, to='wagtailcore.Page', help_text=b'Link to Wagtail overview page for this menu item (leave blank if there is no overview page).', null=True, verbose_name=b'Overview page link'),
        ),
    ]
