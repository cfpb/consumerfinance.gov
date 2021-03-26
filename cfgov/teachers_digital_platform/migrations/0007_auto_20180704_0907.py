# -*- coding: utf-8 -*-
from django.db import migrations, models
import teachers_digital_platform.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0006_auto_20180704_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitypage',
            name='topic',
            field=teachers_digital_platform.fields.ParentalTreeManyToManyField(to='teachers_digital_platform.ActivityTopic'),
        ),
    ]
