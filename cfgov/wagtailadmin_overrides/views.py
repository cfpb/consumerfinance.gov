from django.urls import path

from wagtail.admin.viewsets.base import ViewSet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from ask_cfpb.views import GlossaryTermViewSet
from v1.views.snippets import (
    ContactViewSet,
    EmailSignUpViewSet,
    PortalCategoryViewSet,
    PortalTopicViewSet,
    ReusableNotificationViewSet,
    ReusableTextViewSet,
)

from .search import SearchResultsView, SearchView


class SnippetsViewSetGroup(SnippetViewSetGroup):
    """Menu item that overrides the default Wagtail "Snippets" menu.

    The default Wagtail "Snippets" menu includes all snippet models even if
    those models have some other menu item configured for them. We'd prefer
    if the default snippets menu only included those snippets that aren't
    already exposed elsewhere.

    See https://github.com/wagtail/wagtail/issues/11340 for more detail.

    This item is implemented here in the wagtailadmin_overrides app instead
    of in the v1 app because it relies on models from both the v1 and ask_cfpb
    apps. Implementing it in v1 would introduce a circular dependency between
    those apps.
    """

    items = (
        ContactViewSet,
        EmailSignUpViewSet,
        GlossaryTermViewSet,
        PortalCategoryViewSet,
        PortalTopicViewSet,
        ReusableTextViewSet,
        ReusableNotificationViewSet,
    )
    menu_icon = "snippet"
    menu_label = "Snippets"


class SearchViewSet(ViewSet):
    add_to_admin_menu = True
    menu_label = "Super search"
    icon = "search"
    name = "super-search"

    def get_urlpatterns(self):
        return [
            path("", SearchView.as_view(), name="search"),
            path("results/", SearchResultsView.as_view(), name="results"),
        ]
