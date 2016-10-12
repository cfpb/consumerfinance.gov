# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    """Deprecated migration. See scripts.migrate_job_pages."""
    dependencies = [
        ('jobmanager', '0007_create_careers_pages'),
    ]

    operations = []
