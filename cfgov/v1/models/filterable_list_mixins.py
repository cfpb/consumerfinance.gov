from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Site
from wagtailsharing.models import ShareableRoutablePageMixin

from v1.documents import FilterablePagesDocumentSearch
from v1.feeds import FilterableFeed
from v1.models.learn_page import AbstractFilterPage
from v1.util.ref import get_category_children


class FilterableListMixin(ShareableRoutablePageMixin):
    """Wagtail Page mixin that allows for filtering of other pages."""

    filterable_per_page_limit = 25
    """Number of results to return per page."""

    do_not_index = False
    """Determines whether we tell crawlers to index the page or not."""

    filterable_categories = None
    """Used for activity-log and newsroom to determine
       which pages to render when sitewide"""

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

    def get_filterable_list_wagtail_block(self):
        """Find a FilterableList StreamField block in a content field."""
        return next(
            (b for b in self.content if b.block_type == "filter_controls"),
            None,
        )

    def get_filterable_search(self):
        # By default, filterable pages only search their direct children.
        # But this can be overriden by a setting on a FilterableList block
        # added to the page's content StreamField.
        if filter_block := self.get_filterable_list_wagtail_block():
            children_only = filter_block.value.get("filter_children", True)
        else:
            children_only = True

        # If searching globally, use the root page of this page's Wagtail
        # Site. If the page doesn't live under a Site (for example, it is
        # in the Trash), use the default Site.
        if not children_only:
            site = self.get_site()

            if not site:
                site = Site.objects.get(is_default_site=True)

            search_root = site.root_page
        else:
            search_root = self

        search_cls = self.get_search_class()
        return search_cls(search_root, children_only)

    def get_cache_key_prefix(self):
        return self.url

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        form_data, has_active_filters = self.get_form_data(request.GET)
        filterable_search = self.get_filterable_search()
        has_unfiltered_results = filterable_search.count() > 0
        form = self.get_form_class()(
            form_data,
            wagtail_block=self.get_filterable_list_wagtail_block(),
            filterable_categories=self.filterable_categories,
            filterable_search=filterable_search,
            cache_key_prefix=self.get_cache_key_prefix(),
        )
        filter_data = self.process_form(request, form)

        context.update(
            {
                "filter_data": filter_data,
                "has_active_filters": has_active_filters,
                "has_unfiltered_results": has_unfiltered_results,
            }
        )

        return context

    def process_form(self, request, form):
        filter_data = {}
        if form.is_valid():
            paginator = Paginator(
                form.get_page_set(), self.filterable_per_page_limit
            )
            page = request.GET.get("page")

            # Get the page number in the request and get the page from the
            # paginator to serve.
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)

            filter_data["page_set"] = pages
        else:
            paginator = Paginator([], self.filterable_per_page_limit)
            filter_data["page_set"] = paginator.page(1)

        filter_data["form"] = form
        return filter_data

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
            ]:  # noqa: B950
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
        context = self.get_context(request)
        return FilterableFeed(self, context)(request)


class CategoryFilterableMixin:
    filterable_categories = []
    """Determines page categories to be filtered; see filterable_pages."""

    def get_filterable_search(self):
        """Return the queryset of pages to be filtered by this page.

        The class property filterable_categories can be set to a list of page
        categories from the set in v1.util.ref.categories. If set, this page
        will only filter pages that are tagged with a tag in those categories.
        By default this is an empty list and all page tags are eligible.
        """
        search = super().get_filterable_search()
        category_names = get_category_children(self.filterable_categories)
        search.filter_categories(categories=category_names)
        return search
