# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0008_add_state_and_metro_area_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mortgagedataconstant',
            name='string_value',
        ),
        migrations.AddField(
            model_name='mortgagedataconstant',
            name='date_value',
            field=models.DateField(help_text='CHOOSE THE LAST MONTH OF DATA TO DISPLAY (AND SELECT THE FIRST DAY OF THAT MONTH)', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mortgagedataconstant',
            name='slug',
            field=models.CharField(help_text='OPTIONAL SLUG', max_length=255, blank=True),
        ),
    ]
