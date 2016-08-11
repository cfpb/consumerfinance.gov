# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantTypeSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant_type_label', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['applicant_type_label'],
                'verbose_name': 'Job applicant type',
                'verbose_name_plural': 'Job applicant types',
            },
        ),
    ]
