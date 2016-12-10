from django import template

from v1.models import CFGOVUserPagePermissionsProxy
from wagtail.wagtailcore.models import Page

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
def v1page_permissions(context, page):
    page = page.specific
    if 'user_page_permissions' not in context:
        context['user_page_permissions'] = CFGOVUserPagePermissionsProxy(context['request'].user)

    return context['user_page_permissions'].for_page(page)
