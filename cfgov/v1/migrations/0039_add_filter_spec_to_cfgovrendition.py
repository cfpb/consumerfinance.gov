# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0038_convert_bureau_structure_to_wagtail'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovrendition',
            name='filter_spec',
            field=models.CharField(default='', max_length=255, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cfgovrendition',
            name='filter',
            field=models.ForeignKey(related_name='+', blank=True, to='wagtailimages.Filter', null=True),
        ),
    ]
