from wagtail.wagtailcore import hooks
from wagtail.wagtailusers.widgets import UserListingButton

from django.utils.translation import ugettext_lazy as _
# from django.core.urlresolvers import reverse
from django.conf.urls import include, url

from permissions_viewer import views


@hooks.register('register_admin_urls')
def register_admin_urls():

    urls = [
        url(r'^permissions/user/([^\/]+)/',
            views.display_user_permissions,
            name='user_permissions'),
        url(r'^roster/([^\/]+)/',
            views.display_group_roster,
            name='group_roster'),
    ]
    return urls


@hooks.register('register_user_listing_buttons')
def user_listing_buttons(context, user):
    yield UserListingButton(
        _('View Permissions'),
        '/admin/permissions/user/%s/' % user.pk,
        attrs={'title': _('View permissions for this user')}, priority=15)
