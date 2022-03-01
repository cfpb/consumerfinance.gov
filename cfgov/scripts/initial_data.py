import logging
import os

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction

from wagtail.core.models import Page, Site
from wagtailsharing.models import SharingSite

from v1.models import HomePage


logger = logging.getLogger(__name__)


@transaction.atomic
def run():
    logger.info("Running script initial_data")
    default_site = Site.objects.get(is_default_site=True)

    admin_username = os.getenv("DJANGO_ADMIN_USERNAME")
    admin_password = os.getenv("DJANGO_ADMIN_PASSWORD")
    http_port = int(os.getenv("DJANGO_HTTP_PORT", default_site.port))

    wagtail_sharing_hostname = os.getenv("WAGTAIL_SHARING_HOSTNAME")

    # If specified in the environment, create or activate superuser.
    if admin_username and admin_password:
        logger.info("Configuring superuser, username: {}".format(admin_username))

        User.objects.update_or_create(
            username=admin_username,
            defaults={
                "password": make_password(admin_password),
                "is_superuser": True,
                "is_staff": True,
                "is_active": True,
            },
        )

    # Create home page if it doesn't exist already.
    try:
        home_page = HomePage.objects.get(slug="cfgov")
    except HomePage.DoesNotExist:
        logger.info("Creating new cfgov home page")

        # Create the new home page instance.
        home_page = HomePage(title="CFGov", slug="cfgov", live=True)

        # Add the new home page as a child to the Wagtail root page.
        root_page = Page.objects.get(slug="root")
        root_page.add_child(instance=home_page)

        # Delete the legacy Wagtail "hello world" page, if it exists.
        # This page is created as part of the default Wagtail install.
        # https://github.com/wagtail/wagtail/blob/master/wagtail/core/migrations/0002_initial_data.py#L29
        try:
            hello_world = Page.objects.get(slug="home", url_path="/home/")
        except Page.DoesNotExist:
            pass
        else:
            logger.info("Deleting default Wagtail home page")
            hello_world.delete()

    # If needed, configure the default Wagtail Site to point to the proper
    # home page with the desired port.
    if default_site.root_page_id != home_page.id or default_site.port != http_port:
        default_site.root_page_id = home_page.id
        default_site.port = http_port
        default_site.save()
        logger.info("Configured default Wagtail Site: {}".format(default_site))

    # Setup a sharing site for the default Wagtail site if a sharing hostname
    # has been configured in the environment.
    if wagtail_sharing_hostname:
        sharing_site, _ = SharingSite.objects.update_or_create(
            site=default_site,
            defaults={
                "hostname": wagtail_sharing_hostname,
                "port": http_port,
            },
        )
        logger.info("Configured wagtail-sharing site: {}".format(sharing_site))
