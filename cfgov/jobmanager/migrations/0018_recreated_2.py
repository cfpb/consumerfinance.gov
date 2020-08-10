# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
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
        ('jobmanager', '0017_recreated'),
        ('v1', '0198_recreated'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobListingPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('description', core_fields.RichTextField(verbose_name='Summary')),
                ('open_date', models.DateField(verbose_name='Open date')),
                ('close_date', models.DateField(verbose_name='Close date')),
                ('salary_min', models.DecimalField(verbose_name='Minimum salary', max_digits=11, decimal_places=2)),
                ('salary_max', models.DecimalField(verbose_name='Maximum salary', max_digits=11, decimal_places=2)),
                ('allow_remote', models.BooleanField(default=False, help_text='Adds remote option to jobs with office locations.', verbose_name='Location can also be remote')),
                ('responsibilities', core_fields.RichTextField(null=True, verbose_name='Responsibilities', blank=True)),
                ('travel_required', models.BooleanField(default=False, help_text='Optional: Check to add a "Travel required" section to the job description. Section content defaults to "Yes".')),
                ('travel_details', core_fields.RichTextField(help_text='Optional: Add content for "Travel required" section.', null=True, blank=True)),
                ('additional_section_title', models.CharField(help_text='Optional: Add title for an additional section that will display at end of job description.', max_length=255, null=True, blank=True)),
                ('additional_section_content', core_fields.RichTextField(help_text='Optional: Add content for an additional section that will display at end of job description.', null=True, blank=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobCategory', null=True)),
                ('job_length', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Position length', blank=True, to='jobmanager.JobLength', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='JobLocation',
            fields=[
                ('abbreviation', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('abbreviation',),
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_type', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['service_type'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('name', models.CharField(max_length=255, verbose_name='State name')),
                ('abbreviation', models.CharField(max_length=2, serialize=False, primary_key=True)),
            ],
            options={
                'ordering': ('abbreviation',),
            },
        ),
        migrations.CreateModel(
            name='USAJobsApplicationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('announcement_number', models.CharField(max_length=128)),
                ('url', models.URLField(max_length=255)),
                ('applicant_type', models.ForeignKey(related_name='usajobs_application_links', to='jobmanager.ApplicantType', on_delete=models.CASCADE)),
                ('job_listing', modelcluster.fields.ParentalKey(related_name='usajobs_application_links', to='jobmanager.JobListingPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('joblocation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jobmanager.JobLocation')),
            ],
            options={
                'abstract': False,
            },
            bases=('jobmanager.joblocation',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('joblocation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jobmanager.JobLocation')),
            ],
            options={
                'abstract': False,
            },
            bases=('jobmanager.joblocation',),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='location',
            field=models.ForeignKey(related_name='job_listings', on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobLocation'),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='jobmanager.ServiceType', null=True),
        ),
        migrations.AddField(
            model_name='gradepanel',
            name='grade',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='grade_panels', to='jobmanager.Grade'),
        ),
        migrations.AddField(
            model_name='gradepanel',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='grades', to='jobmanager.JobListingPage'),
        ),
        migrations.AddField(
            model_name='emailapplicationlink',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='email_application_links', to='jobmanager.JobListingPage'),
        ),
        migrations.AddField(
            model_name='city',
            name='location',
            field=modelcluster.fields.ParentalKey(related_name='cities', to='jobmanager.JobLocation'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='cities', default=None, to='jobmanager.State'),
        ),
        migrations.AddField(
            model_name='state',
            name='region',
            field=modelcluster.fields.ParentalKey(related_name='states', to='jobmanager.Region'),
        ),
    ]
