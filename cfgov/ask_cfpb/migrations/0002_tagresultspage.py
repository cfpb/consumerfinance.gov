# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.contrib.wagtailroutablepage.models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagResultsPage',
            fields=[
                ('answerresultspage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ask_cfpb.AnswerResultsPage')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'ask_cfpb.answerresultspage'),
        ),
    ]
