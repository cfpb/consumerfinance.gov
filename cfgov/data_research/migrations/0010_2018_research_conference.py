# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import jsonfield.fields
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data_research', '0009_add_constant_date_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conferenceregistration',
            old_name='code',
            new_name='govdelivery_code',
        ),
        migrations.RemoveField(
            model_name='conferenceregistration',
            name='accommodations',
        ),
        migrations.RemoveField(
            model_name='conferenceregistration',
            name='email',
        ),
        migrations.RemoveField(
            model_name='conferenceregistration',
            name='foodinfo',
        ),
        migrations.RemoveField(
            model_name='conferenceregistration',
            name='name',
        ),
        migrations.RemoveField(
            model_name='conferenceregistration',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='conferenceregistration',
            name='sessions',
        ),
        migrations.AddField(
            model_name='conferenceregistration',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conferenceregistration',
            name='details',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
    ]
