from django.core.paginator import Paginator
from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import route
from wagtail.models import Site

from wagtailsharing.models import ShareableRoutablePageMixin

from v1.documents import FilterablePagesDocumentSearch
from v1.feeds import FilterableFeed
from v1.models.learn_page import AbstractFilterPage
from v1.util.ref import get_category_children


class SearchResultsPaginator(Paginator):
    def _get_page(self, object_list, *args, **kwargs):
        if object_list and object_list.to_queryset:
            object_list = (
                object_list.to_queryset()
                .specific()
                .live()
                .prefetch_related("authors", "categories", "tags")
            )

        return super()._get_page(object_list, *args, **kwargs)


class AbstractFilterablePage(ShareableRoutablePageMixin, models.Model):
    """Wagtail Page class that allows for filtering of other pages."""

    filterable_per_page_limit = 25
    """Number of results to return per page."""

    do_not_index = False
    """Determines whether we tell crawlers to index the page or not."""

    filterable_categories = None
    """Used to restrict filterable results to certain page categories."""

    filterable_results_compact = False
    """Use a compact display to render filtered results."""

    DEFAULT_ORDERING = "-start_date"
    filtered_ordering = models.CharField(
        max_length=30,
        choices=[
            ("-start_date", "Date"),
            ("title.raw", "Alphabetical"),
        ],
        default=DEFAULT_ORDERING,
    )
    filter_children_only = models.BooleanField(
        default=True,
    )

    show_filtered_dates = models.BooleanField(default=True)
    filtered_date_label = models.CharField(
        null=True,
        blank=True,
        max_length=30,
    )
    show_filtered_categories = models.BooleanField(default=True)
    show_filtered_tags = models.BooleanField(default=True)

    class Meta:
        abstract = True

    filtering_panels = [
        MultiFieldPanel(
            [
                FieldPanel("filtered_ordering", heading="Order results by"),
                FieldPanel(
                    "filter_children_only",
                    heading="Only include child pages in results",
                ),
            ],
            heading="Filtering behavior",
        ),
        MultiFieldPanel(
            [
                FieldPanel("show_filtered_dates", heading="Show dates"),
                FieldPanel(
                    "filtered_date_label",
                    heading=(
                        'Date label, e.g. "Published", "Issued", "Released"'
                    ),
                ),
                FieldPanel(
                    "show_filtered_categories", heading="Show categories"
                ),
                FieldPanel("show_filtered_tags", heading="Show tags"),
            ],
            heading="Results display",
        ),
    ]

    @staticmethod
    def get_model_class():
        return AbstractFilterPage

    @staticmethod
    def get_form_class():
        from v1.forms import FilterableListForm

        return FilterableListForm

    @staticmethod
    def get_search_class():
        return FilterablePagesDocumentSearch

    def get_filterable_search(self):
        # If searching globally, use the root page of this page's Wagtail Site.
        # If the page doesn't live under a Site, use the default Site.
        if not self.filter_children_only:
            site = self.get_site()

            if not site:
                site = Site.objects.get(is_default_site=True)

            search_root = site.root_page
        else:
            search_root = self

        search_cls = self.get_search_class()
        search = search_cls(
            search_root,
            children_only=self.filter_children_only,
            ordering=self.filtered_ordering,
        )

        if self.filterable_categories:
            search.filter_categories(
                get_category_children(self.filterable_categories)
            )

        return search

    def get_cache_key_prefix(self, request=None):
        return self.get_url(request=request)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        form_data, has_active_filters = self.get_form_data(request.GET)
        filterable_search = self.get_filterable_search()
        has_unfiltered_results = filterable_search.count() > 0

        form = self.get_form_class()(
            form_data,
            filterable_search=filterable_search,
            cache_key_prefix=self.get_cache_key_prefix(request),
        )
        form_valid = form.is_valid()

        context.update(
            {
                "form": form,
                "form_valid": form_valid,
                "has_unfiltered_results": has_unfiltered_results,
                "has_active_filters": has_active_filters,
            }
        )

        if form_valid:
            context.update(**self.get_valid_form_results(request, form))

        return context

    def get_valid_form_results(self, request, form):
        filtered_qs = form.get_page_set()
        paginator = SearchResultsPaginator(
            filtered_qs, self.filterable_per_page_limit
        )
        filtered_qs_page = paginator.get_page(request.GET.get("page"))

        from v1.serializers import FilterPageSerializer

        serializer = FilterPageSerializer(
            filtered_qs_page, many=True, context={"request": request}
        )

        return {
            "paginator": paginator,
            "page_number": filtered_qs_page.number,
            "results": serializer.data,
        }

    def set_do_not_index(self, field, value):
        """Do not index queries unless they consist of a single topic field."""
        if field != "topics" or len(value) > 1:
            self.do_not_index = True

    # Set up the form's data either with values from the GET request
    # or with defaults based on whether it's a dropdown/list or a text field
    def get_form_data(self, request_dict):
        form_data = {}
        has_active_filters = False
        for field in self.get_form_class().declared_fields:
            if field in [
                "categories",
                "topics",
                "language",
                "statuses",
                "products",
            ]:  # noqa: E501
                value = request_dict.getlist(field, [])
            else:
                value = request_dict.get(field, "")
            if value:
                form_data[field] = value
                has_active_filters = True
                self.set_do_not_index(field, value)
        return form_data, has_active_filters

    def render(self, request, *args, **kwargs):
        """Render with optional X-Robots-Tag in response headers"""
        response = super().render(request, *args, **kwargs)

        # Set noindex for crawlers if needed
        if self.do_not_index:
            response["X-Robots-Tag"] = "noindex"

        return response

    def serve(self, request, *args, **kwargs):
        # Set a cache key for this filterable list page.
        # We do this in `serve()` so that it gets applied to all routes, not
        # just routes that use `render()`.
        response = super().serve(request, *args, **kwargs)
        response["Edge-Cache-Tag"] = self.slug
        return response

    @route(r"^$")
    def index_route(self, request):
        return self.render(request)

    @route(r"^feed/$")
    def feed_route(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)

        view = FilterableFeed(request, self, context["results"])
        response = view(request, *args, **kwargs)

        # Tell Akamai that the feed should have a maximum age of 10 minutes.
        response["Edge-Control"] = "cache-maxage=10m"

        return response
