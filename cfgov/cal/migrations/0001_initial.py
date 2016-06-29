# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CFPBCalendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CFPBCalendarEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=255, blank=True)),
                ('dtstart', models.DateTimeField()),
                ('dtend', models.DateTimeField()),
                ('dtstamp', models.DateTimeField()),
                ('sequence', models.IntegerField(default=0)),
                ('recurrence_id', models.CharField(max_length=255, null=True, blank=True)),
                ('created', models.DateTimeField(blank=True)),
                ('all_day', models.BooleanField(default=False)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('calendar', models.ForeignKey(to='cal.CFPBCalendar')),
            ],
        ),
        migrations.CreateModel(
            name='CFPBPDFFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CFPBImportICSFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cal.cfpbcalendar',),
        ),
    ]
