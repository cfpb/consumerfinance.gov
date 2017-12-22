# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0097_move_reusable_text_chooser_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='feature_flag_name',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='show_draft_with_feature_flag',
            field=models.BooleanField(default=False, help_text=b"Whether a this page's latest draft will appear when the selected feature flag is enabled", verbose_name=b'show draft with feature flag'),
        ),
    ]
