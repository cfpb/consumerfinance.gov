# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0087_add_mortgage_chart_block_to_browsepage'),
        ('data_research', '0004_add_valid_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='MortgageChartPage',
            fields=[
                ('browsepage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.BrowsePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.browsepage',),
        ),
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
            },
        ),
    ]
