# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, transaction
from v1.util.migrations import get_or_create_page, get_page


@transaction.atomic
def create_careers_pages(apps, schema_editor):
    home_page = get_page(apps, slug='cfgov')

    about_us_page = get_or_create_page(
        apps,
        page_cls_app='v1',
        page_cls_name='LandingPage',
        title='About Us',
        slug='about-us',
        parent_page=home_page
    )

    careers_page = get_or_create_page(
        apps,
        page_cls_app='v1',
        page_cls_name='SublandingPage',
        title='Careers',
        slug='careers',
        parent_page=about_us_page
    )

    child_pages = [
        ('BrowsePage', 'Working at the CFPB', 'working-at-cfpb'),
        ('BrowsePage', 'Job Application Process', 'application-process'),
        ('BrowsePage', 'Students and Graduates', 'students-and-graduates'),
        ('BrowsePage', 'Current Openings', 'current-openings'),
    ]

    for i, (page_cls_name, title, slug) in enumerate(child_pages):
        get_or_create_page(
            apps,
            page_cls_app='v1',
            page_cls_name=page_cls_name,
            title=title,
            slug=slug,
            parent_page=careers_page
        )


class Migration(migrations.Migration):
    dependencies = [
        ('jobmanager', '0006_auto_20160815_1705'),
        ('v1', '0009_site_root_data'),
    ]

    operations = [
        migrations.RunPython(create_careers_pages, migrations.RunPython.noop),
    ]
