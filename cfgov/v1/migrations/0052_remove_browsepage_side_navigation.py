# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0051_abstractfilterpage_preview_link_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='browsepage',
            name='side_navigation',
        ),
    ]
