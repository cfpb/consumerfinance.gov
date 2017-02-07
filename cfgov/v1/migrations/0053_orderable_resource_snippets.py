# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0052_add_image_inset'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='order',
            field=models.PositiveSmallIntegerField(help_text=b'Snippets will be listed alphabetically by title in a Snippet List module, unless any in the list have a number in this field; those with an order value will appear at the bottom of the list, in ascending order.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='v1.ResourceTag', blank=True, help_text=b'Tags can be used to filter snippets in a Snippet List.', verbose_name='Tags'),
        ),
    ]
