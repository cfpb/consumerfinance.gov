# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0004_add_valid_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='MortgageMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('json_value', models.TextField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Mortgage metadata',
            },
        ),
    ]
