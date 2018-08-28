# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0015_rename_regpage_part_related_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effectiveversion',
            name='effective_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
