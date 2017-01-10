from django.conf.urls import include, url
from django.core.urlresolvers import reverse

from wagtail.wagtailcore import hooks

from workflow.models import WorkflowDestinationSetting
from workflow import urls


class WorkflowUserBarItem(object):

    def __init__(self, destination, page):

        self.destination = destination
        self.page = page

    def render(self, request):
        migrate_url = reverse('workflow:migrate_to_site',
                              args=(self.page.pk, self.destination.pk))
        return "<a href='%s'>Migrate to %s</a>" % (migrate_url,
                                                   self.destination)


@hooks.register('construct_wagtail_userbar')
def add_workflow_bar_items(request, items):
    # Is there a better way to infer the page? Maybe, but this seems pretty
    # robust.
    for bar_item in items:
        if hasattr(bar_item, 'page'):
            current_page = bar_item.page

    # sloppy assumption for demo purposes: the domain you are using is the
    # source "site"
    destination = request.site.workflowdestinationsetting.destination
    if destination:
        items.append(WorkflowUserBarItem(destination,current_page))


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^workflow/', include(urls, app_name='workflow', namespace='workflow')),
    ]
