from django import template
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
    return page.permissions_for_user(context['request'].user)
