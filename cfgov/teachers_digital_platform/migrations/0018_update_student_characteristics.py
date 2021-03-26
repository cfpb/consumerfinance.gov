# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):
    """The automatic data load in this migration has been removed.

    See repository instructions to manually load data.
    """

    dependencies = [
        ('teachers_digital_platform', '0017_change_special_pop_to_student_chars'),
    ]

    operations = [
        migrations.RunPython(migrations.RunPython.noop),
    ]
