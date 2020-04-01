from django.utils.translation import ugettext_lazy as _

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from wagtail.users.widgets import UserListingButton


try:
    from django.urls import include, re_path, reverse
except ImportError:
    from django.conf.urls import include, url as re_path
    from django.core.urlresolvers import reverse


@hooks.register('register_admin_urls')
def register_admin_urls():

    urls = [
        re_path(r'^permissions/', include((
            'permissions_viewer.urls',
            'permissions_viewer'),
            namespace='permissions')
        ),
    ]
    return urls


@hooks.register('register_settings_menu_item')
def register_settings_menu_item():
    return MenuItem('Permissions', reverse('permissions:index'),
                    classnames='icon icon-unlocked')


@hooks.register('register_user_listing_buttons')
def user_listing_buttons(context, user):
    yield UserListingButton(
        _('View Permissions'),
        reverse('permissions:user', args=[user.pk]),
        attrs={'title': _('View permissions for this user')}, priority=15)
