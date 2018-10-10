from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.core.urlresolvers import reverse

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from search.views import SearchView


@hooks.register('register_admin_urls')
def register_external_links_url():
    return [url(
        r'^external-links/$', SearchView.as_view(), name='external-links'
    )]


@hooks.register('register_admin_menu_item')
def register_external_links_menu():
    return MenuItem('External links',
                    reverse('external-links'),
                    classnames='icon icon-link',
                    order=10000)


