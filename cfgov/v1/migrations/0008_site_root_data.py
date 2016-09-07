# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import migrations, transaction
from v1.util.migrations import get_or_create_page


@transaction.atomic
def create_site_root(apps, schema_editor):
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')

    staging_hostname = os.environ['DJANGO_STAGING_HOSTNAME']
    http_port = os.environ['DJANGO_HTTP_PORT']

    root = Page.objects.get(slug='root')

    # Create a new site root with slug 'cfgov' if it doesn't exist already.
    site_root = get_or_create_page(
        apps,
        page_cls_app='v1',
        page_cls_name='HomePage',
        title='CFGov',
        slug='cfgov',
        parent_page=root,
        live=True,
        shared=True
    )

    # Make sure default site (either the one installed with Wagtail, or one
    # that has since been manually setup) is running on the correct port and
    # with the expected home page as its root.
    default_site = Site.objects.get(is_default_site=True)
    default_site.port = http_port
    default_site.root_page_id = site_root.id
    default_site.save()

    # Setup a staging site if it doesn't exist already. Use the correct
    # hostname and port, and the same root home page.
    staging_site, created = Site.objects.get_or_create(
        hostname=staging_hostname,
        defaults={
            'port': http_port,
            'root_page_id': site_root.id,
        }
    )
    staging_site.save()

    # Delete the legacy Wagtail "hello world" page, if it exists.
    try:
        hello_world = Page.objects.get(slug='home')
    except Page.DoesNotExist:
        pass
    else:
        hello_world.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0001_initial'),
        ('v1', '0007_imagetext5050_sharing'),
        ('wagtailcore', '0028_merge'),
    ]

    operations = [
        migrations.RunPython(create_site_root),
    ]
