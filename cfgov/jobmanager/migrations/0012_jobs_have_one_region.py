# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations, models
import django.db.models.deletion


HQ_REGION_ABBREVIATION = 'HQ'


def check_prerequisites(apps, schema_editor):
    JobListingPage = apps.get_model('jobmanager', 'JobListingPage')
    Location = apps.get_model('jobmanager', 'Location')

    # Assert all jobs have at least one region.
    for page in JobListingPage.objects.all():
        if not page.regions.exists():
            raise RuntimeError('cannot migrate page without region')

    # Assert that the headquarters region exists, if any jobs do.
    if JobListingPage.objects.exists():
        Location.objects.get(region=HQ_REGION_ABBREVIATION)


def create_jobregions(apps, schema_editor):
    JobRegion = apps.get_model('jobmanager', 'JobRegion')
    Location = apps.get_model('jobmanager', 'Location')

    for location in Location.objects.all():
        JobRegion.objects.create(
            abbreviation=location.region,
            name=location.region_long
        )


def create_locations(apps, schema_editor):
    JobRegion = apps.get_model('jobmanager', 'JobRegion')
    Location = apps.get_model('jobmanager', 'Location')

    for job_region in JobRegion.objects.all():
        Location.objects.create(
            description=job_region.name,
            region=job_region.abbreviation,
            region_long=job_region.name
        )


def multiple_regions_to_single_region(apps, schema_editor):
    JobListingPage = apps.get_model('jobmanager', 'JobListingPage')
    JobRegion = apps.get_model('jobmanager', 'JobRegion')

    hq_region = JobRegion.objects.get(abbreviation=HQ_REGION_ABBREVIATION)
    for job_listing in JobListingPage.objects.all():
        if 1 < job_listing.regions.count():
            new_region = hq_region
        else:
            old_region = job_listing.regions.get().region
            new_region = JobRegion.objects.get(abbreviation=old_region.region)

        new_region.job_listings.add(job_listing)

        for revision in job_listing.revisions.all():
            content = json.loads(revision.content_json)
            content.pop('regions', None)
            content['region'] = new_region.pk
            revision.content_json = json.dumps(content)
            revision.save()


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0011_delete_fellowshipupdatelist'),
    ]

    operations = [
        migrations.RunPython(check_prerequisites),
        migrations.CreateModel(
            name='JobRegion',
            fields=[
                ('abbreviation', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('abbreviation',),
            },
        ),
        migrations.RunPython(create_jobregions),
        migrations.AddField(
            model_name='joblistingpage',
            name='region',
            field=models.ForeignKey(related_name='job_listings', on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobRegion', null=True),
        ),
        migrations.RunPython(multiple_regions_to_single_region),
        migrations.AlterField(
            model_name='joblistingpage',
            name='region',
            field=models.ForeignKey(related_name='job_listings', on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobRegion'),
        ),
        migrations.RemoveField(
            model_name='regionpanel',
            name='job_listing',
        ),
        migrations.RemoveField(
            model_name='regionpanel',
            name='region',
        ),
        migrations.DeleteModel(
            name='RegionPanel',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
