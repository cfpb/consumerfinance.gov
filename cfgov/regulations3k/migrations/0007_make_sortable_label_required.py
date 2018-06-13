# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0006_set_sortable_label_subpart_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='sortable_label',
            field=models.CharField(max_length=255),
        ),
    ]
