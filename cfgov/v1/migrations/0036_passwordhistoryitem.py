# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0035_cfgovpage_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordHistoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('expires_at', models.DateTimeField()),
                ('locked_until', models.DateTimeField()),
                ('encrypted_password', models.CharField(max_length=128, verbose_name='password')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
