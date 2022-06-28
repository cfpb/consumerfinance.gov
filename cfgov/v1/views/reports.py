from datetime import date

from django.db.models import Case, IntegerField, Value, When

from wagtail.admin.views.reports import PageReportView, ReportView
from wagtail.core.fields import StreamField
from wagtail.core.models import get_page_models
from wagtail.documents.models import Document
from wagtail.images import get_image_model

from v1.models import CFGOVPage
from v1.query import StreamBlockPageQuerySet


def process_categories(queryset):
    """Prep the set of categories associated with a page."""
    return ", ".join([cat.get_name_display() for cat in queryset])


def process_tags(queryset):
    """Prep the set of tags assocaited with a document or page."""
    return ", ".join([tag for tag in queryset])


def construct_absolute_url(url):
    """Turn a relative URL into an absolute URL"""
    return "https://www.consumerfinance.gov" + url


def generate_filename(type):
    """Get a dated filename for an exported spreadsheet."""
    return f"wagtail-report_{type}_{date.today()}"


class PageMetadataReportView(PageReportView):
    header_icon = "doc-empty-inverse"
    title = "Metadata for live pages"

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

    template_name = "v1/page_metadata_report.html"

    def get_filename(self):
        return generate_filename("pages")

    def get_queryset(self):
        return CFGOVPage.objects.filter(live=True).prefetch_related(
            "tags", "categories"
        )


class DocumentsReportView(ReportView):
    header_icon = "doc-full"
    title = "All documents"

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

    template_name = "v1/documents_report.html"

    def get_filename(self):
        return generate_filename("documents")

    def get_queryset(self):
        return Document.objects.all().order_by("-id").prefetch_related("tags")


class ImagesReportView(ReportView):
    header_icon = "image"
    title = "All images"

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

    template_name = "v1/images_report.html"

    def get_filename(self):
        return generate_filename("images")

    def get_queryset(self):
        return (
            get_image_model()
            .objects.all()
            .order_by("-created_at")
            .prefetch_related("tags")
        )


class EmailSignupReportView(PageReportView):
    header_icon = "mail"
    title = "Pages with email signups"

    list_export = PageReportView.list_export + [
        "url",
        "email_signup_value",
    ]
    export_headings = dict(
        [
            ("url", "URL"),
            ("email_signup_value", "Email Signup"),
        ],
        **PageReportView.export_headings,
    )

    custom_field_preprocess = {
        "categories.all": {
            "csv": process_categories,
            "xlsx": process_categories,
        }
    }

    template_name = "v1/page_emailsignups_report.html"

    def get_filename(self):
        return generate_filename("pages_with_email_signups")

    def get_models_with_block(self, target_block):
        for page_cls in get_page_models():
            if page_cls._meta.abstract:
                continue  # pragma: no cover

            for field in page_cls._meta.get_fields(include_parents=False):
                if not isinstance(field, StreamField):
                    continue

                yield page_cls, field.name

    def get_queryset(self):
        # We're diving deep into Django's ORM here.

        # We're going to be getting individual querysets for each model with an
        # email_signup block in its streamfields. We'll select only the pk and
        # annotate with the email_signup block's value. Annotating after
        # values() will add the annotation to the resulting values dict.
        querysets = [
            (
                StreamBlockPageQuerySet(model)
                .live()
                .block_in_field("email_signup", field)
                .values("pk")
                .annotate_block_in("email_signup", field)
            )
            for model, field in self.get_models_with_block("email_signups")
        ]

        # Then we're going to union those to get one big queryset with all page
        # pks and their email_signup block values.
        qs = querysets[0].union(*querysets[1:])

        # Unfortunately, we need to evaluate this queryset now. We can't do the
        # email_signup_value annotation on our final queryset unless we do.
        page_pks_and_email_signup_values = list(qs)

        # We're going to pull out the page pks, for use in filter() in our
        # final queryset.
        page_pks = [d["pk"] for d in page_pks_and_email_signup_values]

        # Next we're going to construct a list of SQL WHEN statements for use
        # in our annotation on the final queryset. This will express the list
        # of page pks and email_signup_values in SQL form and allow us to
        # attached the email_signup_value as an annotation on the new queryset.
        email_signup_value_whens = [
            When(pk=d["pk"], then=Value(d["email_signup_value"]))
            for d in page_pks_and_email_signup_values
        ]

        # Now we construct our final queryset. This will be for any CFGOVPage
        # object with a pk in our list of page_pks, and then we'll annotate
        # that queryset with our email_signup_value_whens.
        page_qs = CFGOVPage.objects.filter(pk__in=page_pks).annotate(
            email_signup_value=Case(
                *email_signup_value_whens, output_field=IntegerField()
            )
        )

        return page_qs
