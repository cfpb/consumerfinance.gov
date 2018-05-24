# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0003_alter_regulationpage_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='effectiveversion',
            name='acquired',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='effectiveversion',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]
