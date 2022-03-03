# -*- coding: utf-8 -*-
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('teachers_digital_platform', '0014_update_building_blocks'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitypage',
            name='handout_file_3',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Student file 3', blank=True, to='wagtaildocs.Document', null=True),
        ),
        migrations.AlterField(
            model_name='activitypage',
            name='activity_file',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Teacher guide', to='wagtaildocs.Document', null=True),
        ),
        migrations.AlterField(
            model_name='activitypage',
            name='handout_file',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Student file 1', blank=True, to='wagtaildocs.Document', null=True),
        ),
        migrations.AlterField(
            model_name='activitypage',
            name='handout_file_2',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Student file 2', blank=True, to='wagtaildocs.Document', null=True),
        ),
    ]
