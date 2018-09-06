# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0016_require_effective_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effectiveversion',
            name='created',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
