# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('key', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('enabled_by_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FlagState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=False)),
                ('flag', models.ForeignKey(related_name='states', to='flags.Flag')),
                ('site', models.ForeignKey(related_name='flag_states', to='wagtailcore.Site')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='flagstate',
            unique_together=set([('flag', 'site')]),
        ),
    ]
