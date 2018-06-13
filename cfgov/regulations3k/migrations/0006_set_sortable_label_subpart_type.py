# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from regulations3k.models import sortable_label


def forwards(apps, schema_editor):
    Subpart = apps.get_model("regulations3k", "Subpart")
    for subpart in Subpart.objects.all():
        if 'appendi' in subpart.label.lower():
            subpart.subpart_type = 1000
        elif 'interp' in subpart.label.lower():
            subpart.subpart_type = 2000
        subpart.save()

    Section = apps.get_model("regulations3k", "Section")
    for section in Section.objects.all():
        # Save the section again to apply our sortable label logic
        section.sortable_label = '-'.join(sortable_label(section.label))
        section.save()


def backwards(apps, schema_editor):
    # There's no need to go backwards, because these fields will simply
    # disappear with no loss of information that's captured with existing
    # fields.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0005_add_sortable_label_subpart_type'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
