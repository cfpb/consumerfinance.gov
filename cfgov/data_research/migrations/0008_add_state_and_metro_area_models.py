# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0007_add_non_msa_model'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='countymortgagedata',
            name='fips_type',
        ),
        migrations.RemoveField(
            model_name='countymortgagedata',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='msamortgagedata',
            name='counties',
        ),
        migrations.RemoveField(
            model_name='msamortgagedata',
            name='fips_type',
        ),
        migrations.RemoveField(
            model_name='msamortgagedata',
            name='states',
        ),
        migrations.RemoveField(
            model_name='msamortgagedata',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='nationalmortgagedata',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='nonmsamortgagedata',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='statemortgagedata',
            name='valid',
        ),
        migrations.AddField(
            model_name='county',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='data_research.State', null=True),
        ),
        migrations.AddField(
            model_name='countymortgagedata',
            name='county',
            field=models.ForeignKey(to='data_research.County', null=True),
        ),
        migrations.AddField(
            model_name='msamortgagedata',
            name='msa',
            field=models.ForeignKey(to='data_research.MetroArea', null=True),
        ),
        migrations.AddField(
            model_name='nonmsamortgagedata',
            name='state',
            field=models.ForeignKey(to='data_research.State', null=True),
        ),
        migrations.AddField(
            model_name='statemortgagedata',
            name='state',
            field=models.ForeignKey(to='data_research.State', null=True),
        ),
    ]
