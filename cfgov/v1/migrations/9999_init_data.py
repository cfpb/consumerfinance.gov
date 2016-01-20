# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import migrations, models
from django.conf import settings

from ..models.events import EventLandingPage
from ..models.base import CFGOVPage

from wagtail.wagtailcore.models import Page


def initial_data(apps, schema_editor):
    if settings.DEBUG:
        admin_user = User(username='admin',
                          password=make_password(os.environ.get('WAGTAIL_ADMIN_PW')),
                          is_superuser=True, is_active=True, is_staff=True)
        admin_user.save()

        # Renaming Site root name to `V1`
        site_root = Page.objects.get(id=2)
        site_root.title = 'V1'
        site_root.save()

        # Events Landing Page required for event `import-data` command
        events = EventLandingPage(title='Events', slug='events')
        site_root.add_child(instance=events)
        revision = events.save_revision(
            user=admin_user,
            submitted_for_moderation=False,
        )
        revision.publish()


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0034_failedloginattempt'),
    ]

    operations = [
        migrations.RunPython(initial_data)
    ]
