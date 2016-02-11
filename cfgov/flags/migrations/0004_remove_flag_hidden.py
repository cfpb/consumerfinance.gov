# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0003_flag_hidden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flag',
            name='hidden',
        ),
    ]
