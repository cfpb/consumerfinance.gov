# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class MySQLOnlyRunSQL(migrations.RunSQL):
    def _run_sql(self, schema_editor, sqls):
        if schema_editor.connection.vendor.startswith('mysql'):
            super(MySQLOnlyRunSQL, self)._run_sql(schema_editor, sqls)


class Migration(migrations.Migration):
    dependencies = [
        ('jobmanager', '0001_initial'),
    ]

    operations = [
        MySQLOnlyRunSQL([
            (
                'ALTER TABLE jobmanager_job '
                'DEFAULT CHARACTER SET utf8 COLLATE utf8_bin'
            ),
            (
                'ALTER TABLE jobmanager_job '
                'CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin'
            )
        ]),
    ]
