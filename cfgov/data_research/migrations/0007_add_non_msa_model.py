# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0006_mortgageperformancepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonMSAMortgageData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fips', models.CharField(db_index=True, max_length=6, blank=True)),
                ('date', models.DateField(db_index=True, blank=True)),
                ('total', models.IntegerField(null=True)),
                ('current', models.IntegerField(null=True)),
                ('thirty', models.IntegerField(null=True)),
                ('sixty', models.IntegerField(null=True)),
                ('ninety', models.IntegerField(null=True)),
                ('other', models.IntegerField(null=True)),
                ('valid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='mortgagemetadata',
            name='json_value',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
