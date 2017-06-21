# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0069_add_social_sharing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='reusabletext',
            name='sidefoot_heading',
            field=models.CharField(help_text=b'If this snippet is only for use in sidebars and prefooters (aka the "sidefoot"), you can use this field to give it a heading with "slug" styling. See https://[GHE]/flapjack/Modules-V1/wiki/Atoms#slugs', max_length=255, blank=True),
        ),
    ]
