# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):
    """The automatic data load in this migration has been removed.

    See repository instructions to manually load data.
    """

    dependencies = [
        ('teachers_digital_platform', '0015_auto_20180816_0954'),
    ]

    operations = [
        migrations.RunPython(migrations.RunPython.noop),
    ]
