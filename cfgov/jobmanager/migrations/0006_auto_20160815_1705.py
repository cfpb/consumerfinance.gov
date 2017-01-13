# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0005_auto_20160815_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradepanel',
            name='grade',
            field=models.ForeignKey(related_name='grade_panels', to='jobmanager.Grade'),
        ),
        migrations.AlterField(
            model_name='regionpanel',
            name='region',
            field=models.ForeignKey(related_name='region_panels', to='jobmanager.Location'),
        ),
    ]
