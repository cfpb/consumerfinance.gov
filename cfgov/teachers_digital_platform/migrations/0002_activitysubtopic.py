# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivitySubTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(related_name='subtopics', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='teachers_digital_platform.ActivityTopic', null=True)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
    ]
