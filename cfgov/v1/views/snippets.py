from wagtail.snippets.views.snippets import SnippetViewSet

from v1.models import Banner
from wagtailadmin_overrides.ui import BooleanColumn


class BannerViewSet(SnippetViewSet):
    model = Banner
    icon = "warning"
    list_display = ["title", "url_pattern", BooleanColumn("enabled")]
    ordering = ["title"]
    search_fields = ["title", "url_pattern", "content"]
    add_to_admin_menu = True
