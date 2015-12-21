import os, itertools

from django.http import Http404
from django.contrib.auth.models import Permission

from wagtail.wagtailcore import hooks

from v1.models import CFGOVPage


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def share_the_page(request, page):
    page = page.specific
    parent_page = page.get_ancestors(inclusive=False).reverse()[0].specific
    parent_page_perms = parent_page.permissions_for_user(request.user)

    is_publishing = bool(request.POST.get('action-publish')) and parent_page_perms.can_publish()
    is_sharing = bool(request.POST.get('action-share')) and parent_page_perms.can_publish()

    if is_sharing or is_publishing:
        page.shared = True
    else:
        page.shared = False

    page.save()
    revision = page.save_revision()
    if is_publishing:
        revision.publish()


@hooks.register('before_serve_page')
def check_request_site(page, request, serve_args, serve_kwargs):
    if request.site.hostname == os.environ.get('STAGING_HOSTNAME'):
        if isinstance(page, CFGOVPage):
            if not page.shared:
                raise Http404


@hooks.register('register_permissions')
def register_share_permissions():
    return Permission.objects.filter(codename='share_page')
