# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0005_mortgagechartpage_mortgagemetadata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mortgagemetadata',
            options={'ordering': ['name'], 'verbose_name_plural': 'Mortage metadata'},
        ),
    ]
