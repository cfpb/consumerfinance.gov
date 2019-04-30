# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from v1.util.events import get_venue_coords


def forwards(apps, schema_editor):
    EventPage = apps.get_model('v1', 'EventPage')
    for page in EventPage.objects.all():
        page.venue_coords = get_venue_coords(page.venue_city, page.venue_state)
        page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0154_eventpage_venue_coords'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
