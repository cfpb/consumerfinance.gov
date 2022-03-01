from django.urls import reverse

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from search.views import SearchView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


@hooks.register("register_admin_urls")
def register_external_links_url():
    return [re_path(r"^external-links/$", SearchView.as_view(), name="external-links")]


@hooks.register("register_admin_menu_item")
def register_external_links_menu():
    return MenuItem(
        "External links",
        reverse("external-links"),
        classnames="icon icon-link",
        order=10000,
    )
