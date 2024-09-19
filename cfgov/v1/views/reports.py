import html
from datetime import date
from functools import partial
from operator import itemgetter

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import html as html_util

from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import PageReportView, ReportView
from wagtail.documents.models import Document
from wagtail.images import get_image_model
from wagtail.models import Site

import django_filters
from bs4 import BeautifulSoup

from ask_cfpb.models.answer_page import AnswerPage
from v1.models import CFGOVPage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.util.ref import categories, get_category_icon


def process_categories(queryset):
    """Prep the set of categories associated with a page."""
    return ", ".join([cat.get_name_display() for cat in queryset])


def process_tags(queryset):
    """Prep the set of tags assocaited with a document or page."""
    return ", ".join([tag for tag in queryset])


def process_related_item(related_item, key):
    value = getattr(related_item, key) if related_item else ""
    return str(value)


def join_values_with_pipe(queryset, key):
    value_list = []
    for item in queryset:
        value_list.append(str(getattr(item, key)))
    joined_attributtes = " | ".join(value_list)
    return joined_attributtes


def strip_html(content):
    unescaped = html.unescape(content)
    return html_util.strip_tags(unescaped).strip()


def process_enforcement_action_page_content(page_content):
    content = ""
    soup = BeautifulSoup(str(page_content), "html.parser")
    para = soup.findAll(["p", "h5"])
    for p in para:
        content += p.get_text()
        link = p.find("a", href=True)
        if link:
            content += ": "
            content += link["href"]
        content += "\n"
    return content


def construct_absolute_url(url):
    """Turn a relative URL into an absolute URL"""
    return "https://www.consumerfinance.gov" + url


def generate_filename(type):
    """Get a dated filename for an exported spreadsheet."""
    return f"wagtail-report_{type}_{date.today()}"


class PageMetadataReportView(PageReportView):
    header_icon = "doc-empty-inverse"
    page_title = "Page Metadata (for Live Pages)"

    list_export = PageReportView.list_export + [
        "url",
        "first_published_at",
        "last_published_at",
        "language",
        "search_description",
        "tags.names",
        "categories.all",
        "content_owners.names",
    ]
    export_headings = dict(
        [
            ("url", "URL"),
            ("first_published_at", "First published"),
            ("last_published_at", "Last published"),
            ("language", "Language"),
            ("search_description", "Search description"),
            ("tags.names", "Tags"),
            ("categories.all", "Categories"),
            ("content_owners.names", "Content Owner(s)"),
        ],
        **PageReportView.export_headings,
    )

    custom_field_preprocess = {
        "categories.all": {
            "csv": process_categories,
            "xlsx": process_categories,
        }
    }

    index_url_name = "page_metadata_report"
    index_results_url_name = "page_metadata_report_results"
    results_template_name = "v1/page_metadata_report.html"

    def get_filename(self):
        return generate_filename("pages")

    def get_queryset(self):
        return CFGOVPage.objects.filter(live=True).prefetch_related(
            "tags", "categories"
        )


class DraftReportView(PageReportView):
    header_icon = "doc-empty"
    page_title = "Draft Pages"

    list_export = PageReportView.list_export + [
        "url",
        "language",
        "tags.names",
        "categories.all",
        "content_owners.names",
        "first_published_at",
    ]
    export_headings = dict(
        [
            ("url", "URL"),
            ("language", "Language"),
            ("tags.names", "Tags"),
            ("categories.all", "Categories"),
            ("content_owners.names", "Content Owner(s)"),
            ("first_published_at", "Published?"),
        ],
        **PageReportView.export_headings,
    )

    custom_field_preprocess = {
        "categories.all": {
            "csv": process_categories,
            "xlsx": process_categories,
        }
    }

    index_url_name = "page_drafts_report"
    index_results_url_name = "page_drafts_report_results"
    results_template_name = "v1/page_draft_report.html"

    def get_filename(self):
        return generate_filename("pages")

    def get_queryset(self):
        default_site = Site.objects.get(is_default_site=True)
        return (
            CFGOVPage.objects.in_site(default_site)
            .not_live()
            .prefetch_related("tags", "categories")
        )


class DocumentsReportView(ReportView):
    header_icon = "doc-full"
    page_title = "Documents"

    list_export = [
        "id",
        "title",
        "filename",
        "url",
        "collection",
        "tags.names",
        "created_at",
        "uploaded_by_user",
    ]
    export_headings = {
        "id": "ID",
        "title": "Title",
        "filename": "File",
        "url": "URL",
        "collection": "Collection",
        "tags.names": "Tags",
        "created_at": "Uploaded on",
        "uploaded_by_user": "Uploaded by",
    }

    custom_field_preprocess = {
        "tags.names": {"csv": process_tags},
        "url": {"csv": construct_absolute_url},
    }

    index_url_name = "documents_report"
    index_results_url_name = "documents_report_results"
    results_template_name = "v1/documents_report.html"

    def get_filename(self):
        return generate_filename("documents")

    def get_queryset(self):
        return Document.objects.all().order_by("-id").prefetch_related("tags")


class ImagesReportView(ReportView):
    header_icon = "image"
    page_title = "Images"

    list_export = [
        "title",
        "file.url",
        "file_size",
        "collection",
        "tags.names",
        "created_at",
        "uploaded_by_user",
    ]
    export_headings = {
        "title": "Title",
        "file.url": "File",
        "file_size": "Size",
        "collection": "Collection",
        "tags.names": "Tags",
        "created_at": "Uploaded on",
        "uploaded_by_user": "Uploaded by",
    }

    custom_field_preprocess = {
        "tags.names": {"csv": process_tags},
    }

    index_url_name = "images_report"
    index_results_url_name = "images_report_results"
    results_template_name = "v1/images_report.html"

    def get_filename(self):
        return generate_filename("images")

    def get_queryset(self):
        return (
            get_image_model()
            .objects.all()
            .order_by("-created_at")
            .prefetch_related("tags")
        )


class EnforcementActionsReportView(ReportView):
    header_icon = "form"
    page_title = "Enforcement Actions"

    list_export = [
        "title",
        "content",
        "categories.all",
        "court",
        "docket_number_string",
        "initial_filing_date",
        "status_strings",
        "product_strings",
        "url",
    ]
    export_headings = {
        "title": "Title",
        "content": "Content",
        "categories.all": "Forum",
        "court": "Court",
        "docket_number_string": "Docket Numbers",
        "initial_filing_date": "Initial Filling",
        "status_strings": "Statuses",
        "product_strings": "Products",
        "url": "URL",
    }

    custom_field_preprocess = {
        "content": {"csv": process_enforcement_action_page_content},
        "categories.all": {"csv": process_categories},
        "url": {"csv": construct_absolute_url},
    }

    index_url_name = "enforcement_report"
    index_results_url_name = "enforcement_report_results"
    results_template_name = "v1/enforcement_actions_report.html"

    def get_filename(self):
        """Get a better filename than the default 'spreadsheet-export'."""
        return f"enforcement-actions-report-{date.today()}"

    def get_queryset(self):
        return EnforcementActionPage.objects.all().prefetch_related(
            "categories", "statutes"
        )


class AskReportView(ReportView):
    header_icon = "help"
    page_title = "Ask CFPB"

    list_export = [
        "answer_base",
        "id",
        "question",
        "title",
        "short_answer",
        "answer_content",
        "search_description",
        "url",
        "live",
        "last_edited",
        "portal_topic.all",
        "primary_portal_topic",
        "portal_category.all",
        "related_questions.all",
        "language",
    ]
    export_headings = {
        "answer_base": "Ask ID",
        "id": "Page ID",
        "question": "Question",
        "title": "Title",
        "short_answer": "Short answer",
        "answer_content": "Answer",
        "search_description": "Meta description",
        "url": "URL",
        "live": "Live",
        "last_edited": "Last edited",
        "portal_topic.all": "Portal topics",
        "primary_portal_topic": "Primary portal topic",
        "portal_category.all": "Portal categories",
        "related_questions.all": "Related questions",
        "language": "Language",
    }

    def process_answer_content(answer_content):
        answer_streamfield = answer_content.raw_data
        answer_text = list(
            filter(lambda item: item["type"] == "text", answer_streamfield)
        )
        if answer_text:
            answer = answer_text[0].get("value").get("content")
        else:
            # If no text block is found,
            # there is either a HowTo or FAQ schema block.
            # Both define a description field, so we'll use that here.
            answer_schema = list(
                filter(
                    lambda item: item["type"] == "how_to_schema"
                    or item["type"] == "faq_schema",
                    answer_streamfield,
                )
            )
            if answer_schema:
                answer = answer_schema[0].get("value").get("description")
            else:
                # This is a question with no answer, possibly a new draft.
                answer = ""
        return strip_html(answer)

    custom_field_preprocess = {
        "answer_base": {"csv": partial(process_related_item, key="id")},
        "short_answer": {"csv": strip_html},
        "answer_content": {"csv": process_answer_content},
        "portal_topic.all": {
            "csv": partial(join_values_with_pipe, key="heading")
        },
        "portal_category.all": {
            "csv": partial(join_values_with_pipe, key="heading")
        },
        "related_questions.all": {
            "csv": partial(join_values_with_pipe, key="id")
        },
    }

    index_url_name = "ask_report"
    index_results_url_name = "ask_report_results"
    results_template_name = "v1/ask_report.html"

    def get_filename(self):
        return generate_filename("ask-cfpb")

    def get_queryset(self):
        return AnswerPage.objects.prefetch_related(
            "portal_topic",
            "portal_category",
            "related_questions",
        ).order_by("language", "-answer_base__id")


class CategoryIconReportView(ReportView):
    page_title = "Category Icons"
    header_icon = "site"
    index_url_name = "category_icons_report"
    index_results_url_name = "category_icons_report_results"
    results_template_name = "v1/category_icon_report.html"
    paginate_by = 0

    list_export = [
        "subcategory",
        "category_slug",
        "category_name",
        "icon",
    ]

    def get_queryset(self):
        return [
            {
                "subcategory": subcategory,
                "category_slug": category_slug,
                "category_name": category_name,
                "icon": get_category_icon(category_name),
            }
            for subcategory, subcategories in categories
            for category_slug, category_name in subcategories
        ]


class TranslatedPagesReportFilterSet(WagtailFilterSet):
    language = django_filters.MultipleChoiceFilter(
        label="Translation",
        method="filter_language",
        choices=[
            (code, name)
            for code, name in sorted(settings.LANGUAGES, key=itemgetter(1))
            if code != "en"
        ],
    )

    def filter_language(self, queryset, name, value):
        if value:
            queryset = queryset.filter(non_english_pages__language__in=value)

        return queryset

    class Meta:
        model = CFGOVPage
        fields = ["language"]


class TranslatedPagesReportView(PageReportView):
    page_title = "Translated Pages"
    header_icon = "site"
    index_url_name = "translated_pages_report"
    index_results_url_name = "translated_pages_report_results"
    results_template_name = "v1/translated_pages_report.html"
    filterset_class = TranslatedPagesReportFilterSet

    def get_queryset(self):
        return CFGOVPage.objects.filter(
            non_english_pages__isnull=False
        ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["languages"] = settings.LANGUAGES
        return context


class ActiveUsersReportView(ReportView):
    page_title = "Active Users"
    header_icon = "user"
    index_url_name = "active_users_report"
    index_results_url_name = "active_users_report_results"
    results_template_name = "v1/active_users_report.html"
    paginate_by = 0

    list_export = [
        "first_name",
        "last_name",
        "username",
        "email",
        "last_login",
    ]

    def get_queryset(self):
        return get_user_model().objects.filter(is_active=True)
