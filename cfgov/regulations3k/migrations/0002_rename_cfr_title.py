# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ['part_number']},
        ),
        migrations.RenameField(
            model_name='part',
            old_name='cfr_title',
            new_name='cfr_title_number',
        ),
        migrations.AlterField(
            model_name='effectiveversion',
            name='part',
            field=models.ForeignKey(related_name='versions', to='regulations3k.Part'),
        ),
        migrations.AlterField(
            model_name='section',
            name='subpart',
            field=models.ForeignKey(related_name='sections', to='regulations3k.Subpart'),
        ),
        migrations.AlterField(
            model_name='subpart',
            name='version',
            field=models.ForeignKey(related_name='subparts', to='regulations3k.EffectiveVersion'),
        ),
    ]
