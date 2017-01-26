# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0004_auto_20160815_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradePanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('grade', models.ForeignKey(related_name='panels', to='jobmanager.Grade')),
            ],
            options={
                'ordering': ('grade',),
            },
        ),
        migrations.CreateModel(
            name='RegionPanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
            ],
            options={
                'ordering': ('region',),
            },
        ),
        migrations.RemoveField(
            model_name='joblistingpage',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='joblistingpage',
            name='region',
        ),
        migrations.AddField(
            model_name='regionpanel',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='regions', to='jobmanager.JobListingPage'),
        ),
        migrations.AddField(
            model_name='regionpanel',
            name='region',
            field=models.ForeignKey(related_name='panels', to='jobmanager.Location'),
        ),
        migrations.AddField(
            model_name='gradepanel',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='grades', to='jobmanager.JobListingPage'),
        ),
    ]
