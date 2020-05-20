# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):
    """The automatic data load in this migration has been removed.

    See repository instructions to manually load data.
    """

    dependencies = [
        ('teachers_digital_platform', '0009_auto_20180718_1442'),
    ]

    operations = [
        migrations.RunPython(migrations.RunPython.noop),
    ]
