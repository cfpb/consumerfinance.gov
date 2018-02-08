# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0014_add_city_and_state'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='applicanttype',
            name='display_title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='additional_section_content',
            field=wagtail.wagtailcore.fields.RichTextField(help_text=b'Optional: Add content for an additional section that will display at end of job description.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='additional_section_title',
            field=models.CharField(help_text=b'Optional: Add title for an additional section that will display at end of job description.', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='responsibilities',
            field=wagtail.wagtailcore.fields.RichTextField(null=True, verbose_name=b'Responsibilities', blank=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='travel_details',
            field=wagtail.wagtailcore.fields.RichTextField(help_text=b'Optional: Add content for "Travel required" section.', null=True, verbose_name=b'Travel details', blank=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='travel_required',
            field=models.BooleanField(default=False, help_text=b'Optional: Check to add a "Travel required" section to the job description. Section content defaults to "Yes".'),
        ),
        migrations.AlterField(
            model_name='joblistingpage',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(verbose_name=b'Summary'),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='job_length',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Position length', blank=True, to='jobmanager.JobLength', null=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='jobmanager.ServiceType', null=True),
        ),
    ]
