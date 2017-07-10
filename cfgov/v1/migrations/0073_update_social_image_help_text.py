# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0072_add_image_and_help_text_to_data_snapshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cfgovpage',
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text=b'Optionally select a custom image to appear when users share this page on social media websites. Minimum size: 1200w x 630h.', null=True),
        ),
    ]
