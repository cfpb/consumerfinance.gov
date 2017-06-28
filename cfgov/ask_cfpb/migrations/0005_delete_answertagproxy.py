# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0004_add_ask_category_images'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AnswerTagProxy',
        ),
    ]
