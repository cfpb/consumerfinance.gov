# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    replaces = [
	('data_research', '0001_initial'),
        ('data_research', '0002_conf_reg_form_code'),
        ('data_research', '0003_county_mortgage_data_models'),
        ('data_research', '0004_add_valid_fields'),
        ('data_research', '0005_mortgagemetadata'),
        ('data_research', '0006_mortgageperformancepage'),
        ('data_research', '0007_add_non_msa_model'),
        ('data_research', '0008_add_state_and_metro_area_models'),
        ('data_research', '0009_add_constant_date_field'),
	('data_research', '0010_2018_research_conference'),
    ]

    dependencies = [
        ('data_research', '0011_recreated'),
        ('v1', '0198_recreated'),
    ]

    operations = [
        migrations.CreateModel(
            name='MortgagePerformancePage',
            fields=[
                ('browsepage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.BrowsePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.browsepage',),
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
                ('msa', models.ForeignKey(to='data_research.MetroArea', null=True)),
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
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fips', models.CharField(db_index=True, max_length=2, blank=True)),
                ('name', models.CharField(db_index=True, max_length=128, blank=True)),
                ('abbr', models.CharField(max_length=2)),
                ('ap_abbr', models.CharField(help_text="The AP Stylebook's state abbreviation", max_length=20)),
                ('counties', jsonfield.fields.JSONField(help_text='FIPS list of counties in the state', blank=True)),
                ('non_msa_counties', jsonfield.fields.JSONField(help_text='FIPS list of counties in the state that are not in an MSA', blank=True)),
                ('msas', jsonfield.fields.JSONField(help_text='FIPS list of MSAs in the state', blank=True)),
                ('non_msa_valid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
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
                ('state', models.ForeignKey(to='data_research.State', null=True)),
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='nonmsamortgagedata',
            name='state',
            field=models.ForeignKey(to='data_research.State', null=True),
        ),
        migrations.AddField(
            model_name='countymortgagedata',
            name='county',
            field=models.ForeignKey(to='data_research.County', null=True),
        ),
        migrations.AddField(
            model_name='county',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='data_research.State', null=True),
        ),
    ]
