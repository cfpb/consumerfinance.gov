# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0007_subcategory_prefixes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['weight'], 'verbose_name_plural': 'subcategories'},
        ),
    ]
