# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('flags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlagState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='site',
        ),
        migrations.RemoveField(
            model_name='flag',
            name='enabled',
        ),
        migrations.RemoveField(
            model_name='flag',
            name='id',
        ),
        migrations.RemoveField(
            model_name='flag',
            name='site',
        ),
        migrations.AlterField(
            model_name='flag',
            name='key',
            field=models.CharField(max_length=255, serialize=False, primary_key=True),
        ),
        migrations.DeleteModel(
            name='SiteSettings',
        ),
        migrations.AddField(
            model_name='flagstate',
            name='flag',
            field=models.ForeignKey(to='flags.Flag'),
        ),
        migrations.AddField(
            model_name='flagstate',
            name='site',
            field=models.ForeignKey(to='wagtailcore.Site'),
        ),
    ]
