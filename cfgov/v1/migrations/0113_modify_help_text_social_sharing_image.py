# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0112_add_menu_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cfgovpage',
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text=b'Optionally select a custom image to appear when users share this page on social media websites. Recommended size: 1200w x 630h. Maximum size: 4096w x 4096h.', null=True),
        ),
    ]
