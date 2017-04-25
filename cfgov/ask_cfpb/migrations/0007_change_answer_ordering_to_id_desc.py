# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb',
         '0006_answercategorypage_secondary_nav_exclude_sibling_pages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-id']},
        ),
    ]
