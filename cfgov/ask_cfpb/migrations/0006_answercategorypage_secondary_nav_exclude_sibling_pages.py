# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0005_add_category_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='answercategorypage',
            name='secondary_nav_exclude_sibling_pages',
            field=models.BooleanField(default=False),
        ),
    ]
