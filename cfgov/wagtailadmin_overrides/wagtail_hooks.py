from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .views import SearchViewSet, SnippetsViewSetGroup


register_snippet(SnippetsViewSetGroup)


@hooks.register("register_admin_viewset")
def register_search_viewset():
    return SearchViewSet()
