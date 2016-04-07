# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0075_auto_20160404_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractfilterpage',
            name='date_published',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
