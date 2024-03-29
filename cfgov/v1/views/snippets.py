from wagtail.admin.ui.tables import BooleanColumn
from wagtail.snippets.views.snippets import SnippetViewSet

from v1.models import (
    Banner,
    Contact,
    EmailSignUp,
    PortalCategory,
    PortalTopic,
    ReusableNotification,
    ReusableText,
)


class BannerViewSet(SnippetViewSet):
    model = Banner
    icon = "warning"
    list_display = ["title", "url_pattern", BooleanColumn("enabled")]
    ordering = ["title"]
    search_fields = ["title", "url_pattern", "content"]
    add_to_admin_menu = True


class ContactViewSet(SnippetViewSet):
    model = Contact
    icon = "snippet"
    list_display = ["heading", "body"]
    ordering = ["heading"]
    search_fields = ["heading", "body", "contact_info"]


class EmailSignUpViewSet(SnippetViewSet):
    model = EmailSignUp
    menu_icon = "snippet"
    list_display = ["topic", "heading", "text", "code", "url"]
    ordering = ["topic"]
    search_fields = ["topic", "code", "url"]


class PortalCategoryViewSet(SnippetViewSet):
    model = PortalCategory
    menu_icon = "snippet"
    list_display = ["heading", "heading_es"]
    ordering = ["heading"]
    search_fields = ["heading", "heading_es"]


class PortalTopicViewSet(SnippetViewSet):
    model = PortalTopic
    menu_icon = "snippet"
    list_display = ["heading", "heading_es"]
    ordering = ["heading"]
    search_fields = ["heading", "heading_es"]


class ReusableTextViewSet(SnippetViewSet):
    model = ReusableText
    menu_icon = "snippet"
    list_display = ["title", "sidefoot_heading", "text"]
    ordering = ["title"]
    search_fields = ["title", "sidefoot_heading", "text"]


class ReusableNotificationViewSet(SnippetViewSet):
    model = ReusableNotification
    menu_icon = "warning"
    list_display = ["title"]
    ordering = ["title"]
    search_fields = ["title", "content"]
