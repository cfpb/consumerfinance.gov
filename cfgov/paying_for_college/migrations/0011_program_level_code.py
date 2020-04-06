# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paying_for_college', '0010_program_median_monthly_debt'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='level_code',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
