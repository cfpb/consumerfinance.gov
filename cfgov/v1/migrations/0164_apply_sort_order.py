# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def apply_display_order(apps, schema_editor):
    initial_display_order = {1: 1, 4: 2, 5: 3, 2: 4, 3: 5}
    PortalCategory = apps.get_model('v1', 'PortalCategory')
    for category in PortalCategory.objects.all():
        category.display_order = initial_display_order[category.pk]
        category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0163_portalcategory_display_order'),
    ]

    operations = [
        migrations.RunPython(apply_display_order),
    ]
