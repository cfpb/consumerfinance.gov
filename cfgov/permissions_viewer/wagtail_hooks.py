from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

try:
    from wagtail.admin.menu import MenuItem
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin.menu import MenuItem
try:
    from wagtail.core import hooks
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore import hooks
try:
    from wagtail.users.widgets import UserListingButton
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailusers.widgets import UserListingButton


@hooks.register('register_admin_urls')
def register_admin_urls():

    urls = [
        url(r'^permissions/',
            include('permissions_viewer.urls',
                    app_name='permissions_viewer',
                    namespace='permissions')),
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
