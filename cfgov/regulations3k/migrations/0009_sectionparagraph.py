# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0008_regulationssearchpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionParagraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paragraph', models.TextField(blank=True)),
                ('paragraph_id', models.CharField(max_length=255, blank=True)),
                ('section', models.ForeignKey(related_name='paragraphs', to='regulations3k.Section')),
            ],
        ),
    ]
