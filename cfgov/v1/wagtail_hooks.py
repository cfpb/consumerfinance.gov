import os

from django.http import Http404
from django.contrib.auth.models import Permission

from wagtail.wagtailcore import hooks

from v1.models import CFGOVPage


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def share_the_page(request, page):
    page = page.specific
    parent_page = page.parent()
    parent_page_perms = parent_page.permissions_for_user(request.user)

    is_publishing = bool(request.POST.get('action-publish')) and parent_page_perms.can_publish()
    is_sharing = bool(request.POST.get('action-share')) and parent_page_perms.can_publish()

    # If the page is being shared or published, set `shared` to True or else False
    # and save the page.
    if is_sharing or is_publishing:
        page.shared = True
    else:
        page.shared = False
    page.save()

    # If the page isn't being published but the page is live and the editor
    # wants to share updated content that doesn't show on the production site,
    # we must set the page.live to True, delete the latest revision, and save
    # a new revision with `live` = False. This doesn't affect the page's published
    # status, as the saved page object in the database still has `live` equal to
    # True and we're never commiting the change. As seen in CFGOVPage's route
    # method, `route()` will select the latest revision of the page where `live`
    # is set to True and return that revision as a page object to serve the request with.
    if not is_publishing:
        page.live = False
    latest = page.get_latest_revision()
    latest.delete()
    revision = page.save_revision()

    # If the page is being published, the publish the newly created revision.
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
