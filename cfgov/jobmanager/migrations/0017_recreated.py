# -*- coding: utf-8 -*-

from django.db import migrations, models

from wagtail.core import fields as core_fields


class Migration(migrations.Migration):

    replaces = [
        ('jobmanager', '0001_initial'),
        ('jobmanager', '0002_auto_20160809_1619'),
        ('jobmanager', '0003_auto_20160814_2044'),
        ('jobmanager', '0004_auto_20160815_1008'),
        ('jobmanager', '0005_auto_20160815_1457'),
        ('jobmanager', '0006_auto_20160815_1705'),
        ('jobmanager', '0007_create_careers_pages'),
        ('jobmanager', '0008_migrate_job_pages'),
        ('jobmanager', '0009_django_cleanup'),
        ('jobmanager', '0010_cleanup_unused_fields'),
        ('jobmanager', '0011_delete_fellowshipupdatelist'),
        ('jobmanager', '0012_jobs_have_one_region'),
        ('jobmanager', '0013_job_region_to_location'),
        ('jobmanager', '0014_add_city_and_state'),
        ('jobmanager', '0015_remove_tinymce'),
        ('jobmanager', '0016_add_job_length_and_service_type'),
    ]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant_type', models.CharField(max_length=255)),
                ('display_title', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['applicant_type'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='City name')),
            ],
            options={
                'ordering': ('state_id', 'name'),
            },
        ),
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
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.CharField(max_length=32)),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
            ],
            options={
                'ordering': ['grade'],
            },
        ),
        migrations.CreateModel(
            name='GradePanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
            ],
            options={
                'ordering': ('grade',),
            },
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_category', models.CharField(max_length=255)),
                ('blurb', core_fields.RichTextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['job_category'],
            },
        ),
        migrations.CreateModel(
            name='JobLength',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_length', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['job_length'],
            },
        ),
    ]
