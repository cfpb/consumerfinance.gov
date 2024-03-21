from wagtail import hooks

from archival.views import PageArchiveView


@hooks.register("before_delete_page")
def archive_before_deletion(request, page):
    """Archive a page with wagtail-bakery before deleting it."""
    PageArchiveView().build_archive(page)
