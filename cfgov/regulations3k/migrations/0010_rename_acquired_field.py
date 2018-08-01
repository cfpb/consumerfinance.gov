# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0009_sectionparagraph'),
    ]

    operations = [
        migrations.RenameField(
            model_name='effectiveversion',
            old_name='acquired',
            new_name='created',
        ),
    ]
