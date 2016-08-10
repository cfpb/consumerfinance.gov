# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def alter_jobmanager_tables(apps, schema_editor):
    migrations.RunSQL([
        'ALTER TABLE jobmanager_job '
        'DEFAULT CHARACTER SET utf8 COLLATE utf8_bin'
    ])

    if 'mysql' == schema_editor.connection.vendor:
        migrations.RunSQL([
            'ALTER TABLE jobmanager_job '
            'CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin'
        ])


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(alter_jobmanager_tables),
    ]
