# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0002_answeraudiencepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='answercategorypage',
            name='ask_subcategory',
            field=models.ForeignKey(related_name='subcategory_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.SubCategory', null=True),
        ),
    ]
