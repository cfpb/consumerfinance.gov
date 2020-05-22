# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ('agreements', '0001_initial'),
        ('agreements', '0002_auto_20160524_1806'),
        ('agreements', '0003_auto_20160608_1533'),
        ('agreements', '0004_auto_20160615_1814'),
    ]

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
