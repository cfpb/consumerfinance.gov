# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0010_cleanup_unused_fields'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FellowshipUpdateList',
        ),
    ]
