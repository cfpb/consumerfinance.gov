# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.contenttypes.models import ContentType


def remove_reversion_ct(apps,schema_editor):
    ContentType.objects.filter(app_label='reversion').delete()

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
            migrations.RunPython(remove_reversion_ct)
    ]
