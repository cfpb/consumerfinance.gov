# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0018_update_student_characteristics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitybuildingblock',
            name='svg_icon',
            field=models.CharField(blank=True, choices=[('settings', 'Executive function'), ('split', 'Financial knowledge and decision making'), ('piggy-bank-check', 'Financial habits and norms')], max_length=60, null=True),
        ),
    ]
