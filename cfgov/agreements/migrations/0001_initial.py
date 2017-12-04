# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.TextField(max_length=255)),
                ('pdf_size', models.IntegerField()),
                ('txt_size', models.IntegerField()),
                ('pdf_uri', models.URLField()),
                ('txt_uri', models.URLField()),
                ('effective_date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=255)),
                ('city', models.TextField(max_length=64)),
                ('state', models.TextField(max_length=2)),
                ('ffiec_regulator', models.TextField(max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='issuer',
            field=models.ForeignKey(to='agreements.Issuer'),
        ),
    ]
