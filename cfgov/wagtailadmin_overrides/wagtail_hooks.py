from wagtail import hooks
from wagtail.admin.userbar import ContentCheckerItem
from wagtail.snippets.models import register_snippet

from wagtailadmin_overrides.views import SnippetsViewSetGroup


register_snippet(SnippetsViewSetGroup)


@hooks.register("construct_wagtail_userbar")
# We only want content checker errors to appear in the page editor preview.
# This hides content checker errors (both inline and in the Wagtail userbar)
# on the front end.
def hide_content_checker_if_not_previewing_page(request, items):
    if not getattr(request, "is_preview", False):
        items[:] = [i for i in items if not isinstance(i, ContentCheckerItem)]
