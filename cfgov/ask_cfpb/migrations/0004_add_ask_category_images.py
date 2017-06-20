# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0069_add_social_sharing_image'),
        ('ask_cfpb', '0003_add_answercategorypage'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text="Optionally select a custom image to appear when users share this page on social media websites. If no image is selected, this page's category image will be used.", null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text='Select a custom image to appear when visitors share pages belonging to this category on social media.', null=True),
        ),
    ]
