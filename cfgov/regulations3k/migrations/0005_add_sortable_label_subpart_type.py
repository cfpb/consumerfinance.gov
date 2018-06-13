# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0004_add_acquired_and_draft_to_effectiveversion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['sortable_label']},
        ),
        migrations.AlterModelOptions(
            name='subpart',
            options={'ordering': ['subpart_type', 'label']},
        ),
        migrations.AddField(
            model_name='section',
            name='sortable_label',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='subpart',
            name='subpart_type',
            field=models.IntegerField(default=0, choices=[(0, 'Regulation Body'), (1000, 'Appendix'), (2000, 'Interpretation')]),
        ),
    ]
