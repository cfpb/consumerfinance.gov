# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0102_recreated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='order',
            field=models.PositiveSmallIntegerField(help_text=b'Snippets will be listed alphabetically by title in a Snippet List module, unless any in the list have a number in this field; those with an order value will appear in ascending order.', null=True, blank=True),
        ),
    ]
