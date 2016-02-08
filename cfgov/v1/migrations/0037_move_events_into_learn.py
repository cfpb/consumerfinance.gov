# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('v1', '0036_browsefilterable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventarchivepage',
            name='cfgovpage_ptr',
        ),
        migrations.AddField(
            model_name='eventarchivepage',
            name='browsefilterablepage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=4L, serialize=False, to='v1.BrowseFilterablePage'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='eventarchivepage',
            name='body',
        ),
        migrations.RemoveField(
            model_name='eventpage',
            name='cfgovpage_ptr',
        ),
        migrations.AddField(
            model_name='eventpage',
            name='abstractlearnpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=5L, serialize=False, to='v1.AbstractLearnPage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='abstractlearnpage',
            name='date_published',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.DeleteModel(
            name='EventLandingPage',
        ),
        migrations.DeleteModel(
            name='EventRequestSpeakerPage',
        ),
    ]
