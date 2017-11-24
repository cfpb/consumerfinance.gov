from django.core.urlresolvers import reverse

from wagtail.wagtailcore.utils import WAGTAIL_APPEND_SLASH

from jinja2 import contextfunction


def get_url_parts_for_site(page, site):
    """
    Determine the URL for a page on a given site and return it as a tuple of
    ``(site_id, site_root_url, page_url_relative_to_site_root)``.
    Return None if the page is not routable under the specified site.

    Adaptation of wagtail.wagtailcore.models.Site.get_url_parts.
    """
    site_root_path = site.root_page.url_path

    if page.url_path.startswith(site_root_path):
        page_path = reverse(
            'wagtail_serve',
            args=(page.url_path[len(site_root_path):],)
        )

        # Remove the trailing slash from the URL reverse generates if
        # WAGTAIL_APPEND_SLASH is False and we're not trying to serve
        # the root path.
        if not WAGTAIL_APPEND_SLASH and page_path != '/':
            page_path = page_path.rstrip('/')

        return (site.id, site.root_url, page_path)


def get_page_relative_url(page, site):
    """
    Return the 'most appropriate' URL for a page as related to a given site;
    a local URL if the site matches, or a fully qualified one otherwise.
    Return None if the page is not routable.

    Adaptation of wagtail.wagtailcore.models.Page.relative_url.
    """
    url_parts = get_url_parts_for_site(page, site)

    if url_parts is None:
        return

    site_id, root_url, page_path = url_parts

    if site_id == site.id:
        return page_path
    else:
        return root_url + page_path


@contextfunction
def get_protected_url(context, page):
    if page:
        request = context['request']

        if page.live:
            url = get_page_relative_url(page, request.site)

            if url:
                return url

    return '#'
