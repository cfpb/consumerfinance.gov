# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0002_auto_20151030_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
