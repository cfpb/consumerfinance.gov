# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):
    """The automatic data load in this migration has been removed.

    See repository instructions to manually load data.
    """

    dependencies = [
        ('youth_activity_search', '0013_activitybuildingblock_svg_icon'),
    ]

    operations = [
        migrations.RunPython(migrations.RunPython.noop),
    ]
