# -*- coding: utf-8 -*-

from django.db import migrations, models
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
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('govdelivery_code', models.CharField(max_length=250)),
                ('details', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fips', models.CharField(db_index=True, max_length=6, blank=True)),
                ('name', models.CharField(max_length=128, blank=True)),
                ('valid', models.BooleanField()),
            ],
        ),
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
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MetroArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fips', models.CharField(db_index=True, max_length=6, blank=True)),
                ('name', models.CharField(max_length=128, blank=True)),
                ('counties', jsonfield.fields.JSONField(help_text='FIPS list of counties in the MSA', blank=True)),
                ('states', jsonfield.fields.JSONField(help_text='FIPS list of states touched by MSA', blank=True)),
                ('valid', models.BooleanField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MortgageDataConstant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(help_text='OPTIONAL SLUG', max_length=255, blank=True)),
                ('value', models.IntegerField(null=True, blank=True)),
                ('date_value', models.DateField(help_text='CHOOSE THE LAST MONTH OF DATA TO DISPLAY (AND SELECT THE FIRST DAY OF THAT MONTH)', null=True, blank=True)),
                ('note', models.TextField(blank=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MortgageMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('json_value', jsonfield.fields.JSONField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Mortgage metadata',
            },
        ),
    ]
