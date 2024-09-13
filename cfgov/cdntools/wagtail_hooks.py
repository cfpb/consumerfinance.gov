from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from cdntools.views import (
    cdn_is_configured,
    manage_cdn,
)


class IfCDNEnabledMenuItem(MenuItem):
    def is_shown(self, request):
        return cdn_is_configured()


@hooks.register("register_admin_menu_item")
def register_cdn_menu_item():
    return IfCDNEnabledMenuItem(
        "CDN Tools",
        reverse("manage-cdn"),
        classname="icon icon-cogs",
        order=10000,
    )


@hooks.register("register_admin_urls")
def register_cdn_url():
    return [
        path("cdn/", manage_cdn, name="manage-cdn"),
    ]
