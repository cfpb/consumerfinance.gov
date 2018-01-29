# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations, models
import django.db.models.deletion


def create_locations(apps, schema_editor):
    JobRegion = apps.get_model('jobmanager', 'JobRegion')
    Office = apps.get_model('jobmanager', 'Office')
    Region = apps.get_model('jobmanager', 'Region')
    
    for region in JobRegion.objects.all():
        if 'region' in region.name:
            Region.objects.update_or_create(
                abbreviation=region.abbreviation,
                name=region.name
            )
        else:
            Office.objects.update_or_create(
                abbreviation=region.abbreviation,
                name=region.name
            )

def add_locations_to_job_listings(apps, schema_editor):
    JobListingPage = apps.get_model('jobmanager', 'JobListingPage')
    JobLocation = apps.get_model('jobmanager', 'JobLocation')

    if not JobListingPage.objects.exists():
        return

    for job_listing in JobListingPage.objects.all():
        if job_listing.region:
            region_abbreviation = job_listing.region.abbreviation
            location = JobLocation.objects.get(abbreviation=region_abbreviation)
            job_listing.location = location
            job_listing.save() 
            
            for revision in job_listing.revisions.all():
                content = json.loads(revision.content_json)
                region = content['region']
                if region:
                    revision_location = JobLocation.objects.get(abbreviation=region)
                    content['location'] = revision_location.pk
                    revision.content_json = json.dumps(content)
                    revision.save()



class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0012_jobs_have_one_region'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='joblistingpage',
            name='allow_remote',
            field=models.BooleanField(default=False, help_text=b'Adds remote option to jobs with office locations.'),
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('joblocation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='jobmanager.JobLocation')),
            ],
            bases=('jobmanager.joblocation',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('joblocation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='jobmanager.JobLocation')),
            ],
            bases=('jobmanager.joblocation',),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='location',
            field=models.ForeignKey(related_name='job_listings', on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobLocation', null=True),
        ),
        migrations.RunPython(create_locations),
        migrations.RunPython(add_locations_to_job_listings),
        migrations.RemoveField(
            model_name='joblistingpage',
            name='region',
        ),
        migrations.DeleteModel(
            name='JobRegion',
        ),
    ]