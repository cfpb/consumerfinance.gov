# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0015_update_email_signup_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text="Optionally select a custom image to appear when users share this page on social media websites. If no image is selected, this page's category image will be used. Recommended size: 1200w x 630h. Maximum size: 4096w x 4096h.", null=True),
        ),
    ]
