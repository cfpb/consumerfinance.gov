# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0068_remove_cfgovrendition_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text=b'Optionally select a custom image to appear when users share this page on social media websites.', null=True),
        ),
    ]
