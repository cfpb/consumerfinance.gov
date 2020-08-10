# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0016_auto_20180829_2323'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActivitySpecialPopulation',
            new_name='ActivityStudentCharacteristics',
        ),
        migrations.RenameField(
            model_name='activitypage',
            old_name='special_population',
            new_name='student_characteristics',
        ),
    ]
