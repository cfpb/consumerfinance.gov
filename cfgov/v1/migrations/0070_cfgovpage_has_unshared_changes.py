# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0069_auto_20160318_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='has_unshared_changes',
            field=models.BooleanField(default=False),
        ),
    ]
