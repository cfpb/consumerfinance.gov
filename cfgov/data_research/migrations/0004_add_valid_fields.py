# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0003_county_mortgage_data_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='countymortgagedata',
            name='valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mortgagedataconstant',
            name='string_value',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='msamortgagedata',
            name='valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nationalmortgagedata',
            name='valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statemortgagedata',
            name='valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mortgagedataconstant',
            name='value',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
