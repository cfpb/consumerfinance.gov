# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0004_auto_20160712_1531'),
        ('jobmanager', '0002_auto_20160809_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailApplicationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('address', models.EmailField(max_length=254)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobListingPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('description', wagtail.wagtailcore.fields.RichTextField(verbose_name=b'Description')),
                ('open_date', models.DateField(verbose_name=b'Open date')),
                ('close_date', models.DateField(verbose_name=b'Close date')),
                ('salary_min', models.DecimalField(verbose_name=b'Minimum salary', max_digits=11, decimal_places=2)),
                ('salary_max', models.DecimalField(verbose_name=b'Maximum salary', max_digits=11, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='USAJobsApplicationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('announcement_number', models.CharField(max_length=128)),
                ('url', models.URLField(max_length=255)),
                ('applicant_type', models.ForeignKey(related_name='usajobs_application_links', to='jobmanager.ApplicantType')),
                ('job_listing', modelcluster.fields.ParentalKey(related_name='usajobs_application_links', to='jobmanager.JobListingPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='emailapplicationlink',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='email_application_links', to='jobmanager.JobListingPage'),
        ),
    ]
