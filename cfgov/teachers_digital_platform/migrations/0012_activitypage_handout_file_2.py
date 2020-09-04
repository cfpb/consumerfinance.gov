# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('teachers_digital_platform', '0011_update_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitypage',
            name='handout_file_2',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True),
        ),
    ]
