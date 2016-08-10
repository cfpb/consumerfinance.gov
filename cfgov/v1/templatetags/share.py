import os
from urlparse import urlparse

from django import template
from wagtail.wagtailcore.models import Page

from v1.models import CFGOVUserPagePermissionsProxy

register = template.Library()


@register.filter
def is_shared(page):
    page = page.specific
    if isinstance(page, Page):
        if page.shared:
            return True
        else:
            return False


@register.assignment_tag(takes_context=True)
def get_page_state_url(context, page):
    page = Page.objects.get(id=page.id).specific
    if not page.live and not page.shared:
        return None
    url = page.url
    if url is None:  # If page is not aligned to a site root return None
        return None
    page_hostname = urlparse(url).hostname
    staging_hostname = os.environ.get('STAGING_HOSTNAME')
    if not page.live and page.shared and staging_hostname != page_hostname:
        url = url.replace(page_hostname, staging_hostname)
    return url


@register.assignment_tag(takes_context=True)
def v1page_permissions(context, page):
    page = page.specific
    if 'user_page_permissions' not in context:
        context['user_page_permissions'] = CFGOVUserPagePermissionsProxy(context['request'].user)

    return context['user_page_permissions'].for_page(page)
