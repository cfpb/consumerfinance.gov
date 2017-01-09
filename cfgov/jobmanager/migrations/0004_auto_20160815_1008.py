# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0003_auto_20160814_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblistingpage',
            name='division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobCategory', null=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobmanager.Grade', null=True),
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobmanager.Location', null=True),
        ),
    ]
