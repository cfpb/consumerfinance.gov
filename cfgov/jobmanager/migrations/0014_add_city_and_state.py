# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0013_job_region_to_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'City name')),
                ('location', modelcluster.fields.ParentalKey(related_name='cities', to='jobmanager.JobLocation')),
            ],
            options={
                'ordering': ('state_id', 'name'),
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('name', models.CharField(max_length=255, verbose_name=b'State name')),
                ('abbreviation', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('region', modelcluster.fields.ParentalKey(related_name='states', to='jobmanager.Region')),
            ],
            options={
                'ordering': ('abbreviation',),
            },
        ),
        migrations.AlterField(
            model_name='joblistingpage',
            name='location',
            field=models.ForeignKey(related_name='job_listings', on_delete=django.db.models.deletion.PROTECT, default='', to='jobmanager.JobLocation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(related_name='cities', default=None, to='jobmanager.State'),
        ),
    ]
