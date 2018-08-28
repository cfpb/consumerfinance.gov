# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import migrations, models


logger = logging.getLogger(__name__)


def site_str(site):
    """Generate a string representation for a Wagtail Site.

    This is needed because models in migrations don't have any of their
    methods (like __str__). This logic is copied from Wagtail.
    """
    if site.site_name:
        return(
            site.site_name +
            (" [default]" if site.is_default_site else "")
        )
    else:
        return(
            site.hostname +
            ("" if site.port == 80 else (":%d" % site.port)) +
            (" [default]" if site.is_default_site else "")
        )


def delete_non_default_wagtail_sites(apps, schema_editor):
    """Deletes all non-default Wagtail Sites from the database.

    For historical reasons we have deployments that have more than one Wagtail
    Site object: a main one and then a duplicate one ("content") which was
    used in the past for sharing draft changes.

    This second site is no longer needed, and so we want to standardize all
    deployments so that they only have a single site.
    """
    Site = apps.get_model('wagtailcore', 'Site')
    non_default_sites = Site.objects.filter(is_default_site=False)

    for site in non_default_sites:
        logger.info('deleting non-default Wagtail site: %s', site_str(site))
        site.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0115_add_menu_item_nav_footer_block'),
    ]

    operations = [
        migrations.RunPython(
            delete_non_default_wagtail_sites,
            migrations.RunPython.noop
        )
    ]
