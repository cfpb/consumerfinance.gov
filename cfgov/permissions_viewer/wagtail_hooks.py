from django.urls import reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.widgets import Button


try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include
    from django.conf.urls import url as re_path


@hooks.register("register_admin_urls")
def register_admin_urls():
    urls = [
        re_path(
            r"^permissions/",
            include(
                ("permissions_viewer.urls", "permissions"),
                namespace="permissions",
            ),
        ),
    ]
    return urls


@hooks.register("register_settings_menu_item")
def register_settings_menu_item():
    return MenuItem(
        "Permissions",
        reverse("permissions:index"),
        icon_name="lock-open",
    )


@hooks.register("register_user_listing_buttons")
def user_listing_buttons(user, request_user):
    yield Button(
        "View Permissions",
        reverse("permissions:user", args=[user.pk]),
        attrs={"title": "View permissions for this user"},
        icon_name="lock-open",
        priority=15,
    )
