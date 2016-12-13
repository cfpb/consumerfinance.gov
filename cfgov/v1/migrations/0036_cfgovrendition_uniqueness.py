# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0035_add_5050_output_to_flc'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cfgovrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
    ]
