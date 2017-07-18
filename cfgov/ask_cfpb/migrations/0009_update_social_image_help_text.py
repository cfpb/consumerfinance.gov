# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0008_fix_verbose_name_plural'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text="Optionally select a custom image to appear when users share this page on social media websites. If no image is selected, this page's category image will be used. Minimum size: 1200w x 630h.", null=True),
        ),
    ]
