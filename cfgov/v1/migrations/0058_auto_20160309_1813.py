# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0057_auto_20160304_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='browsefilterablepage',
            name='secondary_nav_order',
        ),
        migrations.RemoveField(
            model_name='browsepage',
            name='secondary_nav_order',
        ),
    ]
