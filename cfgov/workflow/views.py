import os.path

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from wagtail.wagtailcore.models import Page, Site

from workflow.preflight import preflight_check
from workflow.utils import first_site_for_page


def migrate(request, page_pk, destination_site_pk):
    page = get_object_or_404(Page, pk=page_pk)
    destination_site = get_object_or_404(Site, pk=destination_site_pk)

    current_site_root = first_site_for_page(page).root_page
    new_root = destination_site.root_page
    #import pdb;pdb.set_trace()
    relative_path = page.url_path[len(current_site_root.url_path):]
    new_path = os.path.join(new_root.url_path, relative_path)

    strategy, target = preflight_check(page, new_root, relative_path)
    strategy_text = strategy.__name__.replace('_', ' ')
    if request.method == "GET":
        return render(request, 'workflow/migrate.html', locals())
    elif request.method == "POST":
        result = strategy(target, page, new_root)
        # todo handle failure cases
        # and maybe find a better way to indicate success
        # This takes you to the 'explore' page *containing* the result
        return_url = reverse('wagtailadmin_explore',
                             args=[result.get_parent().pk])
        return redirect(return_url)
