# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0081_related_metadata_date_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reusabletext',
            name='sidefoot_heading',
            field=models.CharField(help_text=b'Applies "slug" style heading. Only for use in sidebars and prefooters (the "sidefoot"). See [GHE]/flapjack/Modules-V1/wiki/Atoms#slugs', max_length=255, blank=True),
        ),
    ]
