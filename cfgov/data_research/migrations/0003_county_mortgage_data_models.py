# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0002_conf_reg_form_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountyMortgageData',
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
                ('fips_type', models.CharField(default='county', max_length=6)),
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MortgageDataConstant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(help_text='CAMELCASE VARIABLE NAME FOR JS', max_length=255, blank=True)),
                ('value', models.IntegerField(null=True)),
                ('note', models.TextField(blank=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MSAMortgageData',
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
                ('fips_type', models.CharField(default='msa', max_length=6)),
                ('counties', models.CharField(help_text='A comma-separated list of FIPS for included counties.', max_length=255, null=True, blank=True)),
                ('states', models.CharField(help_text='A comma-separated list of state abbreviations touched by FIPS for included counties.', max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NationalMortgageData',
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
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StateMortgageData',
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
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
    ]
