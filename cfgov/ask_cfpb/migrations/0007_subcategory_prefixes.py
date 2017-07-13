# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0006_update_help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='subcategory',
            field=models.ManyToManyField(help_text='Choose only subcategories that belong to one of the categories checked above.', to='ask_cfpb.SubCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='update_english_page',
            field=models.BooleanField(default=False, help_text='Check this box to push your English edits to the page for review. This does not publish your edits.', verbose_name='Send to English page for review'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='update_spanish_page',
            field=models.BooleanField(default=False, help_text='Check this box to push your Spanish edits to the page for review. This does not publish your edits.', verbose_name='Send to Spanish page for review'),
        ),
    ]
