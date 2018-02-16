from wagtail.wagtailcore import hooks
from wagtail.wagtailusers.widgets import UserListingButton
from wagtail.wagtailadmin.menu import MenuItem

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf.urls import include, url


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
