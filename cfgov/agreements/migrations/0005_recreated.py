# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.TextField(max_length=500)),
                ('size', models.IntegerField()),
                ('uri', models.URLField(max_length=500)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=500)),
                ('slug', models.TextField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='issuer',
            field=models.ForeignKey(to='agreements.Issuer',
                                    on_delete=models.CASCADE),
        ),
    ]
