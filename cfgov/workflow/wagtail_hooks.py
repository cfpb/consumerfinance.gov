from django.conf.urls import include, url
from django.core.urlresolvers import reverse

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin import widgets as wagtailadmin_widgets


from workflow import urls
from workflow.utils import first_site_for_page


class WorkflowUserBarItem(object):

    def __init__(self, destination, page):
        self.destination = destination
        self.page = page

    def render(self, request):
        migrate_url = reverse('workflow:migrate_to_site',
                              args=(self.page.pk, self.destination.pk))
        return "<a href='%s'>Migrate to %s</a>" % (migrate_url,
                                                   self.destination)


@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    source_site = first_site_for_page(page)
    if source_site and source_site.workflowdestinationsetting.destination:
        destination = source_site.workflowdestinationsetting.destination
        migrate_url = reverse('workflow:migrate_to_site',
                              args=(page.pk, destination.pk))

        yield wagtailadmin_widgets.PageListingButton(
            'Migrate to %s' % destination,
            migrate_url,
            priority=10
        )


@hooks.register('construct_wagtail_userbar')
def add_workflow_bar_items(request, items):
    # Is there a better way to infer the page? Maybe, but this seems pretty
    # robust.
    for bar_item in items:
        if hasattr(bar_item, 'page'):
            current_page = bar_item.page

    # sloppy assumption for demo purposes: the domain you are using is the
    # source "site"
    destination = (hasattr(request, 'site') and
                   request.site.workflowdestinationsetting.destination)
    if destination:
        items.append(WorkflowUserBarItem(destination, current_page))


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^workflow/', include(
            urls, app_name='workflow', namespace='workflow')),
    ]
