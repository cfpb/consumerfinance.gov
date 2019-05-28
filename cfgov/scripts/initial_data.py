import logging
import os

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction

from wagtail.wagtailcore.models import Page, Site
from wagtailsharing.models import SharingSite

from v1.models import HomePage


logger = logging.getLogger(__name__)


@transaction.atomic
def run():
    logger.info('Running script initial_data')
    default_site = Site.objects.get(is_default_site=True)

    admin_username = os.getenv('DJANGO_ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('DJANGO_ADMIN_PASSWORD', 'admin')
    http_port = int(os.getenv('DJANGO_HTTP_PORT', default_site.port))

    staging_hostname = os.getenv('DJANGO_STAGING_HOSTNAME')

    # Create admin user if it doesn't exist already.
    # Update existing one with admin password and active state.
    logger.info('Configuring superuser, username: {}'.format(admin_username))
    User.objects.update_or_create(
        username=admin_username,
        defaults={
            'password': make_password(admin_password),
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
        }
    )

    # Create home page if it doesn't exist already.
    try:
        home_page = HomePage.objects.get(slug='cfgov')
    except HomePage.DoesNotExist:
        logger.info('Creating new cfgov home page')

        # Create the new home page instance.
        home_page = HomePage(
            title='CFGov',
            slug='cfgov',
            live=True
        )

        # Add the new home page as a child to the Wagtail root page.
        root_page = Page.objects.get(slug='root')
        root_page.add_child(instance=home_page)

    # Configure the default Wagtail Site to point to the proper home page
    # with the desired port.
    default_site.root_page_id = home_page.id
    default_site.port = http_port
    default_site.save()
    logger.info('Configured default Wagtail Site: {}'.format(default_site))

    # Delete the legacy Wagtail "hello world" page, if it exists.
    # This page is created as part of the default Wagtail install.
    # https://github.com/wagtail/wagtail/blob/v1.13.4/wagtail/wagtailcore/migrations/0002_initial_data.py#L33
    try:
        hello_world = Page.objects.get(slug='home', url_path='/home/')
    except Page.DoesNotExist:
        pass
    else:
        logger.info('Deleting default Wagtail home page')
        hello_world.delete()

    # Setup a sharing site for the default Wagtail site if a staging hostname
    # has been configured in the environment.
    if staging_hostname:
        sharing_site, _ = SharingSite.objects.update_or_create(
            site=default_site,
            defaults={
                'hostname': staging_hostname,
                'port': http_port,
            }
        )
        logger.info('Configured wagtail-sharing site: {}'.format(sharing_site))
