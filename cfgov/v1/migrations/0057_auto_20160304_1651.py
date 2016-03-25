# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from v1.models.learn_page import DocumentDetailPage
from itertools import chain


def save_revisions(apps, schema_editor):
    DocumentDetailPage = apps.get_model('v1', 'DocumentDetailPage')
    EventPage = apps.get_model('v1', 'EventPage')
    LearnPage = apps.get_model('v1', 'LearnPage')
    
    pages = list(chain(DocumentDetailPage.objects.all(),
                       EventPage.objects.all(),
                       LearnPage.objects.all()))

    for page in pages:
        page.save_revision()


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0056_auto_20160226_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='abstractfilterpage',
            old_name='preview_link_text',
            new_name='secondary_link_text',
        ),
        migrations.RenameField(
            model_name='abstractfilterpage',
            old_name='preview_link_url',
            new_name='secondary_link_url',
        ),
        migrations.RunPython(save_revisions),
    ]
