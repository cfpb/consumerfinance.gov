import logging
import re

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.html import format_html_join

from wagtail.admin.menu import MenuItem
from wagtail.admin.rich_text.converters.editor_html import (
    WhitelistRule as AllowlistRule,
)
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.core.whitelist import attribute_rule

from ask_cfpb.models.snippets import GlossaryTerm
from v1.admin_views import manage_cdn
from v1.models.banners import Banner
from v1.models.portal_topics import PortalCategory, PortalTopic
from v1.models.resources import Resource
from v1.models.snippets import (
    Contact,
    EmailSignUp,
    RelatedResource,
    ReusableText,
)
from v1.template_debug import (
    call_to_action_test_cases,
    featured_content_test_cases,
    heading_test_cases,
    notification_test_cases,
    register_template_debug,
    related_posts_test_cases,
    translation_links_test_cases,
    video_player_test_cases,
)
from v1.views.reports import (
    AskReportView,
    CategoryIconReportView,
    DocumentsReportView,
    EnforcementActionsReportView,
    ImagesReportView,
    PageMetadataReportView,
    TranslatedPagesReportView,
)


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


logger = logging.getLogger(__name__)


@hooks.register("before_delete_page")
def raise_delete_error(request, page):
    raise PermissionDenied("Deletion via POST is disabled")


@hooks.register("before_bulk_action")
def raise_bulk_delete_error(
    request, action_type, objects, action_class_instance
):
    if action_type == "delete":
        raise PermissionDenied("Deletion via POST is disabled")


@hooks.register("after_delete_page")
def log_page_deletion(request, page):
    logger.warning(
        (
            "User {user} with ID {user_id} deleted page {title} "
            "with ID {page_id} at URL {url}"
        ).format(
            user=request.user,
            user_id=request.user.id,
            title=page.title,
            page_id=page.id,
            url=page.url_path,
        )
    )


@hooks.register("insert_global_admin_js")
def global_admin_js():
    js_files = ["apps/admin/js/global.js"]

    js_includes = format_html_join(
        "\n",
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files),
    )

    return js_includes


@hooks.register("insert_editor_css")
def editor_css():
    css_files = [
        "css/form-explainer.css",
        "css/general-enhancements.css",
        "css/heading-block.css",
        "css/model-admin.css",
        "css/table-block.css",
        "css/simple-chart-admin.css",
    ]

    css_includes = format_html_join(
        "\n",
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files),
    )

    return css_includes


@hooks.register("insert_global_admin_css")
def global_admin_css():
    css_files = [
        "css/model-admin.css",
        "css/global.css",
    ]

    css_includes = format_html_join(
        "\n",
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files),
    )

    return css_includes


class PermissionCheckingMenuItem(MenuItem):
    """
    MenuItem that only displays if the user has a certain permission.

    This subclassing approach is recommended by the Wagtail documentation:
    https://docs.wagtail.io/en/stable/reference/hooks.html#register-admin-menu-item
    """

    def __init__(self, *args, **kwargs):
        self.permission = kwargs.pop("permission")
        super().__init__(*args, **kwargs)

    def is_shown(self, request):
        return request.user.has_perm(self.permission)


@hooks.register("register_admin_menu_item")
def register_django_admin_menu_item():
    return MenuItem(
        "Django Admin",
        reverse("admin:index"),
        classnames="icon icon-redirect",
        order=99999,
    )


@hooks.register("register_admin_menu_item")
def register_frank_menu_item():
    return MenuItem(
        "CDN Tools",
        reverse("manage-cdn"),
        classnames="icon icon-cogs",
        order=10000,
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        re_path(r"^cdn/$", manage_cdn, name="manage-cdn"),
    ]


@hooks.register("before_serve_page")
def serve_latest_draft_page(page, request, args, kwargs):
    if page.pk in settings.SERVE_LATEST_DRAFT_PAGES:
        latest_draft = page.get_latest_revision_as_page()
        response = latest_draft.serve(request, *args, **kwargs)
        response["Serving-Wagtail-Draft"] = "1"
        return response


@hooks.register("register_reports_menu_item")
def register_page_metadata_report_menu_item():
    return MenuItem(
        "Page Metadata",
        reverse("page_metadata_report"),
        classnames="icon icon-" + PageMetadataReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_page_metadata_report_url():
    return [
        re_path(
            r"^reports/page-metadata/$",
            PageMetadataReportView.as_view(),
            name="page_metadata_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_documents_report_menu_item():
    return MenuItem(
        "Documents",
        reverse("documents_report"),
        classnames="icon icon-" + DocumentsReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_documents_report_url():
    return [
        re_path(
            r"^reports/documents/$",
            DocumentsReportView.as_view(),
            name="documents_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_enforcements_actions_report_menu_item():
    return MenuItem(
        "Enforcement Actions",
        reverse("enforcement_report"),
        classnames="icon icon-" + EnforcementActionsReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_enforcements_actions_documents_report_url():
    return [
        re_path(
            r"^reports/enforcement-actions/$",
            EnforcementActionsReportView.as_view(),
            name="enforcement_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_images_report_menu_item():
    return MenuItem(
        "Images",
        reverse("images_report"),
        classnames="icon icon-" + ImagesReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_images_report_url():
    return [
        re_path(
            r"^reports/images/$",
            ImagesReportView.as_view(),
            name="images_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_ask_report_menu_item():
    return MenuItem(
        "Ask CFPB",
        reverse("ask_report"),
        classnames="icon icon-" + AskReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_ask_report_url():
    return [
        re_path(
            r"^reports/ask-cfpb/$",
            AskReportView.as_view(),
            name="ask_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_category_icons_report_menu_item():
    return MenuItem(
        "Category Icons",
        reverse("category_icons_report"),
        classnames="icon icon-" + CategoryIconReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_category_icons_report_url():
    return [
        re_path(
            r"^reports/category-icons/$",
            CategoryIconReportView.as_view(),
            name="category_icons_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_translated_pages_report_menu_item():
    return MenuItem(
        "Translated Pages",
        reverse("translated_pages_report"),
        classnames="icon icon-" + TranslatedPagesReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_translated_pages_report_url():
    return [
        re_path(
            r"^reports/translated-pages/$",
            TranslatedPagesReportView.as_view(),
            name="translated_pages_report",
        ),
    ]


@hooks.register("construct_reports_menu")
# Alphabetizie and title case report menu items
def clean_up_report_menu_items(request, report_menu_items):
    cfpb_re = r"CFPB"
    report_menu_items.sort(key=lambda item: item.label)
    for index, item in enumerate(report_menu_items):
        item.label = item.label.title()
        if re.search(cfpb_re, item.label, re.IGNORECASE):
            item.label = re.sub(cfpb_re, "CFPB", item.label, 0, re.IGNORECASE)
        item.order = index


def get_resource_tags():
    tag_list = []

    for resource in Resource.objects.all():
        for tag in resource.tags.all():
            tuple = (tag.slug, tag.name)
            if tuple not in tag_list:
                tag_list.append(tuple)

    return sorted(tag_list, key=lambda tup: tup[0])


class ResourceTagsFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "tags"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "tag"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return get_resource_tags()

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        for tag in get_resource_tags():
            if self.value() == tag[0]:
                return queryset.filter(tags__slug__iexact=tag[0])


class ResourceModelAdmin(ThumbnailMixin, ModelAdmin):
    model = Resource
    menu_label = "Resources"
    menu_icon = "snippet"
    list_display = ("title", "desc", "order", "admin_thumb")
    thumb_image_field_name = "thumbnail"
    thumb_image_filter_spec = "width-100"
    thumb_image_width = None
    ordering = ("title",)
    list_filter = (ResourceTagsFilter,)
    search_fields = ("title",)


@modeladmin_register
class BannerModelAdmin(ModelAdmin):
    model = Banner
    menu_icon = "warning"
    list_display = ("title", "url_pattern", "enabled")
    ordering = ("title",)
    search_fields = ("title", "url_pattern", "content")


class ContactModelAdmin(ModelAdmin):
    model = Contact
    menu_icon = "snippet"
    list_display = ("heading", "body")
    ordering = ("heading",)
    search_fields = ("heading", "body", "contact_info")


class PortalTopicModelAdmin(ModelAdmin):
    model = PortalTopic
    menu_icon = "snippet"
    list_display = ("heading", "heading_es")
    ordering = ("heading",)
    search_fields = ("heading", "heading_es")


class PortalCategoryModelAdmin(ModelAdmin):
    model = PortalCategory
    menu_icon = "snippet"
    list_display = ("heading", "heading_es")
    ordering = ("heading",)
    search_fields = ("heading", "heading_es")


class ReusableTextModelAdmin(ModelAdmin):
    model = ReusableText
    menu_icon = "snippet"
    list_display = ("title", "sidefoot_heading", "text")
    ordering = ("title",)
    search_fields = ("title", "sidefoot_heading", "text")


class RelatedResourceModelAdmin(ModelAdmin):
    model = RelatedResource
    menu_icon = "snippet"
    list_display = ("title", "text")
    ordering = ("title",)
    search_fields = ("title", "text")


class GlossaryTermModelAdmin(ModelAdmin):
    model = GlossaryTerm
    menu_icon = "snippet"
    list_display = ("name_en", "definition_en", "portal_topic")
    ordering = ("name_en",)
    search_fields = ("name_en", "definition_en", "name_es", "definition_es")


class EmailSignUpModelAdmin(ModelAdmin):
    model = EmailSignUp
    menu_icon = "snippet"
    list_display = ("topic", "heading", "text", "code", "url")
    ordering = ("topic",)
    search_fields = ("topic", "code", "url")


class SnippetModelAdminGroup(ModelAdminGroup):
    menu_label = "Snippets"
    menu_icon = "snippet"
    menu_order = 400
    items = (
        ContactModelAdmin,
        ResourceModelAdmin,
        ReusableTextModelAdmin,
        RelatedResourceModelAdmin,
        PortalTopicModelAdmin,
        PortalCategoryModelAdmin,
        GlossaryTermModelAdmin,
        EmailSignUpModelAdmin,
    )


modeladmin_register(SnippetModelAdminGroup)


# Hide default Snippets menu item
@hooks.register("construct_main_menu")
def hide_snippets_menu_item(request, menu_items):
    menu_items[:] = [
        item
        for item in menu_items
        if item.url != reverse("wagtailsnippets:index")
    ]


# The construct_whitelister_element_rules was depricated in Wagtail 2,
# so we'll use register_rich_text_features instead.
# Only applies to Hallo editors, which only remain in our custom
# AtomicTableBlock table cells.
@hooks.register("register_rich_text_features")
def register_span_feature(features):
    allow_html_class = attribute_rule(
        {
            "class": True,
            "id": True,
        }
    )

    # register a feature 'span'
    # which allowlists the <span> element
    features.register_converter_rule(
        "editorhtml",
        "span",
        [
            AllowlistRule("span", allow_html_class),
        ],
    )

    # add 'span' to the default feature set
    features.default_features.append("span")


@hooks.register("register_permissions")
def add_export_feedback_permission_to_wagtail_admin_group_view():
    return Permission.objects.filter(
        content_type__app_label="v1", codename="export_feedback"
    )


register_template_debug(
    "v1",
    "call_to_action",
    "v1/includes/molecules/call-to-action.html",
    call_to_action_test_cases,
)


register_template_debug(
    "v1",
    "featured_content",
    "v1/includes/organisms/featured-content.html",
    featured_content_test_cases,
    extra_js=["featured-content-module.js"],
)


register_template_debug(
    "v1", "heading", "v1/includes/blocks/heading.html", heading_test_cases
)


register_template_debug(
    "v1",
    "notification",
    "v1/includes/molecules/notification.html",
    notification_test_cases,
)


register_template_debug(
    "v1",
    "related_posts",
    "v1/includes/molecules/related-posts.html",
    related_posts_test_cases,
)


register_template_debug(
    "v1",
    "translation_links",
    "v1/includes/molecules/translation-links.html",
    translation_links_test_cases,
)


register_template_debug(
    "v1",
    "video_player",
    "v1/includes/organisms/video-player.html",
    video_player_test_cases,
    extra_js=["video-player.js"],
)
