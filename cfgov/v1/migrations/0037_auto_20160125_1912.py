# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0036_passwordhistoryitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passwordhistoryitem',
            options={'get_latest_by': 'created'},
        ),
        migrations.AlterField(
            model_name='passwordhistoryitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='passwordhistoryitem',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
