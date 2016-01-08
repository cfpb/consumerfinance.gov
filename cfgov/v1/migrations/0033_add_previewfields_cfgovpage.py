# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0032_cfgovimage_cfgovrendition'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='preview_description',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='preview_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', null=True),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='preview_link_text',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='preview_subheading',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='preview_title',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
