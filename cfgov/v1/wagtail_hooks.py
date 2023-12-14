import logging
import re

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.html import format_html_join

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.models import register_snippet

from v1.admin_views import (
    cdn_is_configured,
    manage_cdn,
    redirect_to_internal_docs,
)
from v1.models import InternalDocsSettings
from v1.template_debug import (
    call_to_action_test_cases,
    contact_us_table_test_cases,
    crc_table_test_cases,
    featured_content_test_cases,
    heading_test_cases,
    notification_test_cases,
    register_template_debug,
    related_posts_test_cases,
    table_test_cases,
    translation_links_test_cases,
    video_player_test_cases,
)
from v1.views.reports import (
    ActiveUsersReportView,
    AskReportView,
    CategoryIconReportView,
    DocumentsReportView,
    DraftReportView,
    EnforcementActionsReportView,
    ImagesReportView,
    PageMetadataReportView,
    TranslatedPagesReportView,
)
from v1.views.snippets import BannerViewSet


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


class StaffOnlyMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.is_staff


@hooks.register("register_admin_menu_item")
def register_django_admin_menu_item():
    return StaffOnlyMenuItem(
        "Django Admin",
        reverse("admin:index"),
        classnames="icon icon-redirect",
        order=99999,
    )


class IfCDNEnabledMenuItem(MenuItem):
    def is_shown(self, request):
        return cdn_is_configured()


@hooks.register("register_admin_menu_item")
def register_cdn_menu_item():
    return IfCDNEnabledMenuItem(
        "CDN Tools",
        reverse("manage-cdn"),
        classnames="icon icon-cogs",
        order=10000,
    )


@hooks.register("register_admin_urls")
def register_cdn_url():
    return [
        re_path(r"^cdn/$", manage_cdn, name="manage-cdn"),
    ]


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
def register_page_drafts_report_menu_item():
    return MenuItem(
        "Draft Pages",
        reverse("page_drafts_report"),
        classnames="icon icon-" + DraftReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_page_drafts_report_url():
    return [
        re_path(
            r"^reports/page-drafts/$",
            DraftReportView.as_view(),
            name="page_drafts_report",
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


@hooks.register("register_reports_menu_item")
def register_active_users_report_menu_item():
    return MenuItem(
        "Active Users",
        reverse("active_users_report"),
        classnames="icon icon-" + ActiveUsersReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_active_users_report_url():
    return [
        re_path(
            r"^reports/active-users/$",
            ActiveUsersReportView.as_view(),
            name="active_users_report",
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
            item.label = re.sub(
                cfpb_re, "CFPB", item.label, count=0, flags=re.IGNORECASE
            )
        item.order = index


register_snippet(BannerViewSet)


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
    "contact_us_table",
    "v1/includes/organisms/tables/contact-us.html",
    contact_us_table_test_cases,
)


register_template_debug(
    "v1",
    "crc_table",
    "v1/includes/organisms/tables/consumer-reporting-company.html",
    crc_table_test_cases,
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
    "table",
    "v1/includes/organisms/tables/base.html",
    table_test_cases,
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


@hooks.register("register_admin_urls")
def register_internal_docs_url():
    return [
        re_path(
            r"^internal-docs/$",
            redirect_to_internal_docs,
            name="internal_docs",
        ),
    ]


class InternalDocsMenuItem(MenuItem):
    def is_shown(self, request):
        return bool(InternalDocsSettings.load(request_or_site=request).url)


@hooks.register("register_help_menu_item")
def register_internal_docs_menu_item():
    return InternalDocsMenuItem(
        "Internal documentation",
        reverse("internal_docs"),
        icon_name="help",
        order=1200,
        attrs={"target": "_blank", "rel": "noreferrer"},
        name="internal_docs_menu",
    )
