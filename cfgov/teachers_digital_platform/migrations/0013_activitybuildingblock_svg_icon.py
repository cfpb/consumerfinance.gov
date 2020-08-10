# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0012_activitypage_handout_file_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitybuildingblock',
            name='icon',
        ),
        migrations.AddField(
            model_name='activitybuildingblock',
            name='svg_icon',
            field=models.CharField(blank=True, max_length=60, null=True, choices=[('settings', 'Executive function'), ('split', 'Financial habits and norms'), ('piggy-bank-check', 'Financial knowledge and decision making')]),
        ),
    ]
