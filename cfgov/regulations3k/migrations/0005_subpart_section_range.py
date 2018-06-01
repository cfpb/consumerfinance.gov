# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0004_add_acquired_and_draft_to_effectiveversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='subpart',
            name='section_range',
            field=models.TextField(null=True, blank=True),
        ),
    ]
