import logging
import re

from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, re_path, reverse
from django.utils.html import format_html_join

from wagtail import hooks
from wagtail.admin import messages, widgets
from wagtail.admin.menu import MenuItem
from wagtail.snippets.models import register_snippet

from v1.admin_views import (
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


logger = logging.getLogger(__name__)

languages = dict(settings.LANGUAGES)


@hooks.register("register_page_header_buttons")
def page_header_buttons(page, user, view_name, next_url=None):
    return [
        widgets.Button(
            f"Edit {languages[translation.language]} page",
            f"/admin/pages/{translation.pk}/edit/",
            priority=1000,
            icon_name="globe",
        )
        for translation in page.get_translations()
        if translation.language != page.language
    ]


@hooks.register("after_delete_page")
def log_page_deletion(request, page):
    logger.warning(
        f"User {request.user} with ID {request.user.id} deleted page "
        f"{page.title} with ID {page.id} at URL {page.url_path}"
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


@hooks.register("insert_global_admin_css")
def editor_css():
    css_files = [
        "css/general-enhancements.css",
        "css/heading-block.css",
        "css/expandable-block.css",
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
        classname="icon icon-redirect",
        order=99999,
    )


@hooks.register("register_reports_menu_item")
def register_page_metadata_report_menu_item():
    return MenuItem(
        "Page Metadata",
        reverse("page_metadata_report"),
        classname="icon icon-" + PageMetadataReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_page_metadata_report_url():
    return [
        path(
            "reports/page-metadata/",
            PageMetadataReportView.as_view(),
            name="page_metadata_report",
        ),
        path(
            "reports/page-metadata/results/",
            PageMetadataReportView.as_view(results_only=True),
            name="page_metadata_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_page_drafts_report_menu_item():
    return MenuItem(
        "Draft Pages",
        reverse("page_drafts_report"),
        classname="icon icon-" + DraftReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_page_drafts_report_url():
    return [
        path(
            "reports/page-drafts/",
            DraftReportView.as_view(),
            name="page_drafts_report",
        ),
        path(
            "reports/page-drafts/results/",
            DraftReportView.as_view(results_only=True),
            name="page_drafts_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_documents_report_menu_item():
    return MenuItem(
        "Documents",
        reverse("documents_report"),
        classname="icon icon-" + DocumentsReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_documents_report_url():
    return [
        path(
            "reports/documents/",
            DocumentsReportView.as_view(),
            name="documents_report",
        ),
        path(
            "reports/documents/results/",
            DocumentsReportView.as_view(results_only=True),
            name="documents_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_enforcements_actions_report_menu_item():
    return MenuItem(
        "Enforcement Actions",
        reverse("enforcement_report"),
        classname="icon icon-" + EnforcementActionsReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_enforcements_actions_documents_report_url():
    return [
        path(
            "reports/enforcement-actions/",
            EnforcementActionsReportView.as_view(),
            name="enforcement_report",
        ),
        path(
            "reports/enforcement-actions/results/",
            EnforcementActionsReportView.as_view(results_only=True),
            name="enforcement_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_images_report_menu_item():
    return MenuItem(
        "Images",
        reverse("images_report"),
        classname="icon icon-" + ImagesReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_images_report_url():
    return [
        path(
            "reports/images/",
            ImagesReportView.as_view(),
            name="images_report",
        ),
        path(
            "reports/images/results/",
            ImagesReportView.as_view(results_only=True),
            name="images_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_ask_report_menu_item():
    return MenuItem(
        "Ask CFPB",
        reverse("ask_report"),
        classname="icon icon-" + AskReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_ask_report_url():
    return [
        path(
            "reports/ask-cfpb/",
            AskReportView.as_view(),
            name="ask_report",
        ),
        path(
            "reports/ask-cfpb/results/",
            AskReportView.as_view(results_only=True),
            name="ask_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_category_icons_report_menu_item():
    return MenuItem(
        "Category Icons",
        reverse("category_icons_report"),
        classname="icon icon-" + CategoryIconReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_category_icons_report_url():
    return [
        path(
            "reports/category-icons/",
            CategoryIconReportView.as_view(),
            name="category_icons_report",
        ),
        path(
            "reports/category-icons/results/",
            CategoryIconReportView.as_view(results_only=True),
            name="category_icons_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_translated_pages_report_menu_item():
    return MenuItem(
        "Translated Pages",
        reverse("translated_pages_report"),
        classname="icon icon-" + TranslatedPagesReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_translated_pages_report_url():
    return [
        path(
            "reports/translated-pages/",
            TranslatedPagesReportView.as_view(),
            name="translated_pages_report",
        ),
        path(
            "reports/translated-pages/results/",
            TranslatedPagesReportView.as_view(results_only=True),
            name="translated_pages_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_active_users_report_menu_item():
    return MenuItem(
        "Active Users",
        reverse("active_users_report"),
        classname="icon icon-" + ActiveUsersReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_active_users_report_url():
    return [
        path(
            "reports/active-users/",
            ActiveUsersReportView.as_view(),
            name="active_users_report",
        ),
        path(
            "reports/active-users/results/",
            ActiveUsersReportView.as_view(),
            name="active_users_report_results",
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


@hooks.register("before_delete_page")
def prevent_locked_page_deletion(request, page):
    """Prevent deletion of locked pages"""
    if page.locked:
        messages.warning(
            request, f"{page.title} is locked and cannot be deleted."
        )
        return redirect("wagtailadmin_explore", page.pk)


@hooks.register("before_bulk_action")
def prevent_locked_page_bulk_deletion(
    request, action_type, objects, action_class_instance
):
    """Prevent deletion of locked pages when part of a bulk action"""
    if action_type == "delete":
        for obj in objects:
            if hasattr(obj, "locked") and obj.locked:
                messages.warning(
                    request,
                    f"{obj} is locked and cannot be deleted. "
                    "Please remove it from the selection.",
                )
                if request.META.get("HTTP_REFERER"):
                    return redirect(request.META.get("HTTP_REFERER"))
                return redirect("wagtailadmin_home")
