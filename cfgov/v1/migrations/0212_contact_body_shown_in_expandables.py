# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0211_add_schema_blocks_to_blogpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='body_shown_in_expandables',
            field=models.BooleanField(default=False),
        ),
    ]
