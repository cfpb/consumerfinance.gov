# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0008_migrate_job_pages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='applicant_types',
        ),
        migrations.RemoveField(
            model_name='job',
            name='category',
        ),
        migrations.RemoveField(
            model_name='job',
            name='grades',
        ),
        migrations.RemoveField(
            model_name='job',
            name='locations',
        ),
        migrations.RemoveField(
            model_name='jobapplicanttype',
            name='application_type',
        ),
        migrations.RemoveField(
            model_name='jobapplicanttype',
            name='job',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.DeleteModel(
            name='JobApplicantType',
        ),
    ]
