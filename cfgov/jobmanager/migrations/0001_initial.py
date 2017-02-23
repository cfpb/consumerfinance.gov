# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant_type', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['applicant_type'],
            },
        ),
        migrations.CreateModel(
            name='FellowshipUpdateList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.CharField(max_length=255, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('likes_design', models.BooleanField(default=False)),
                ('likes_cybersecurity', models.BooleanField(default=False)),
                ('likes_development', models.BooleanField(default=False)),
                ('likes_data', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.CharField(max_length=32)),
                ('slug', models.SlugField()),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['grade'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('salary_min', models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)),
                ('salary_max', models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)),
                ('hourly', models.BooleanField(default=False)),
                ('open_date', models.DateField()),
                ('close_date', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField()),
                ('date_modified', models.DateTimeField()),
                ('open_graph_title', models.CharField(help_text=b'If blank, uses the title field above', max_length=255, blank=True)),
                ('open_graph_description', models.CharField(help_text=b'If blank, uses the description field above', max_length=1000, blank=True)),
                ('open_graph_image_url', models.URLField(help_text=b'A full URL to an image. If blank, uses the CFPB logo.', blank=True)),
                ('twitter_text', models.CharField(help_text=b'Custom text for Twitter shares. If blank, uses the first         100 characters of the title field above', max_length=100, blank=True)),
                ('utm_campaign', models.CharField(help_text=b'Use to add a UTM campaign code to the share links         on this page.', max_length=100, verbose_name=b'UTM campaign', blank=True)),
            ],
            options={
                'ordering': ['close_date', 'title'],
            },
        ),
        migrations.CreateModel(
            name='JobApplicantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_usajobs', models.BooleanField(default=True)),
                ('usajobs_url', models.URLField(max_length=255, null=True, blank=True)),
                ('announcement_number', models.CharField(max_length=128, null=True, blank=True)),
                ('announcement_email', models.CharField(max_length=128, null=True, blank=True)),
                ('announcement_close_time', models.TimeField(null=True, blank=True)),
                ('application_type', models.ForeignKey(to='jobmanager.ApplicantType')),
                ('job', models.ForeignKey(to='jobmanager.Job')),
            ],
            options={
                'ordering': ['job'],
            },
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_category', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('blurb', models.TextField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['job_category'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('region', models.CharField(max_length=2)),
                ('region_long', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['region'],
            },
        ),
        migrations.AddField(
            model_name='job',
            name='applicant_types',
            field=models.ManyToManyField(to='jobmanager.ApplicantType', through='jobmanager.JobApplicantType'),
        ),
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.ForeignKey(to='jobmanager.JobCategory'),
        ),
        migrations.AddField(
            model_name='job',
            name='grades',
            field=models.ManyToManyField(to='jobmanager.Grade', verbose_name=b'list of grades'),
        ),
        migrations.AddField(
            model_name='job',
            name='locations',
            field=models.ManyToManyField(to='jobmanager.Location', verbose_name=b'list of locations'),
        ),
    ]
