# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paying_for_college', '0009_expandable_group_help_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='median_monthly_debt',
            field=models.IntegerField(blank=True, help_text='MEDIAN MONTHLY PAYMENT FOR A 10-YEAR LOAN', null=True),
        ),
    ]
