from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from v1.forms import FilterableListForm
from v1.models.learn_page import AbstractFilterPage
from v1.util.ref import get_category_children
from v1.util.util import get_secondary_nav_items


class FilterableListMixin(object):
    """Wagtail Page mixin that allows for filtering of other pages."""

    filterable_categories = []
    """Determines page categories to be filtered; see filterable_pages."""

    filterable_children_only = True
    """Determines page tree to be filtered; see filterable_pages."""

    filterable_per_page_limit = 10
    """Number of results to return per page."""

    do_not_index = False
    """Determines whether we tell crawlers to index the page or not."""

    @staticmethod
    def get_model_class():
        return AbstractFilterPage

    @staticmethod
    def get_form_class():
        return FilterableListForm

    def filterable_pages(self):
        """Return pages that are eligible to be filtered by this page.

        Always includes only live pages and pages that live in the same Wagtail
        site as this page. If this page cannot be mapped to a Wagtail site (for
        example, if it does not live under a site root), then it will not
        return any filterable results.

        The class property filterable_categories can be set to a list of page
        categories from the set in v1.util.ref.categories. If set, this page
        will only filter pages that are tagged with a tag in those categories.
        By default this is an empty list and all page tags are eligible.

        The class property filterable_children_only determines whether this
        page filters only pages that are direct children of this page. By
        default this is True; set this to False to allow this page to filter
        pages that are not direct children of this page.
        """
        site = self.get_site()

        if not site:
            return self.get_model_class().objects.none()

        pages = self.get_model_class().objects.in_site(site).live()

        if self.filterable_categories:
            category_names = get_category_children(self.filterable_categories)
            pages = pages.filter(categories__name__in=category_names)

        if self.filterable_children_only:
            pages = pages.child_of(self)

        return pages

    def filterable_list_wagtail_block(self):
        return next((b for b in self.content if b.block_type == 'filter_controls'), None)  # noqa 501

    def get_context(self, request, *args, **kwargs):
        context = super(FilterableListMixin, self).get_context(
            request, *args, **kwargs
        )

        form_data, has_active_filters = self.get_form_data(request.GET)
        form = self.get_form_class()(
            form_data,
            filterable_pages=self.filterable_pages(),
            wagtail_block=self.filterable_list_wagtail_block(),
        )

        context.update({
            'filter_data': self.process_form(request, form),
            'get_secondary_nav_items': get_secondary_nav_items,
            'has_active_filters': has_active_filters,
        })

        return context

    def process_form(self, request, form):
        filter_data = {}
        if form.is_valid():
            paginator = Paginator(form.get_page_set(),
                                  self.filterable_per_page_limit)
            page = request.GET.get('page')

            # Get the page number in the request and get the page from the
            # paginator to serve.
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)

            filter_data['page_set'] = pages
        else:
            paginator = Paginator([], self.filterable_per_page_limit)
            filter_data['page_set'] = paginator.page(1)
        filter_data['form'] = form
        return filter_data

    def set_do_not_index(self, field, value):
        """Do not index queries unless they consist of a single topic field."""
        if field != 'topics' or len(value) > 1:
            self.do_not_index = True

    # Set up the form's data either with values from the GET request
    # or with defaults based on whether it's a dropdown/list or a text field
    def get_form_data(self, request_dict):
        form_data = {}
        has_active_filters = False
        for field in self.get_form_class().declared_fields:
            if field in ['categories', 'topics', 'authors']:
                value = request_dict.getlist(field, [])
            else:
                value = request_dict.get(field, '')
            if value:
                form_data[field] = value
                has_active_filters = True
                self.set_do_not_index(field, value)
        return form_data, has_active_filters

    def serve(self, request, *args, **kwargs):
        """Modify response headers."""
        response = super(FilterableListMixin, self).serve(request)
        # Set a shorter TTL in Akamai
        response['Edge-Control'] = 'cache-maxage=10m'
        # Set noindex for crawlers if needed
        if self.do_not_index:
            response['X-Robots-Tag'] = 'noindex'
        return response
