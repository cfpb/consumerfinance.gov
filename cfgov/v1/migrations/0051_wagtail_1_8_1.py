# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0050_refactor_chart_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cfgovrendition',
            name='filter_spec',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='cfgovrendition',
            name='focal_point_key',
            field=models.CharField(default='', max_length=16, editable=False, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='cfgovrendition',
            unique_together=set([('image', 'filter_spec', 'focal_point_key')]),
        ),
    ]
