from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from v1.forms import FilterableListForm
from v1.models.base import CFGOVPage
from v1.models.learn_page import AbstractFilterPage
from v1.util.util import get_secondary_nav_items


class FilterableListMixin(object):

    def get_context(self, request, *args, **kwargs):
        context = {}
        try:
            context = super(FilterableListMixin, self).get_context(
                request, *args, **kwargs)
        except AttributeError as e:
            raise e
        context['get_secondary_nav_items'] = get_secondary_nav_items
        form_data, has_active_filters = self.get_form_data(request.GET)
        form = FilterableListForm(form_data, base_query=self.base_query())
        context['has_active_filters'] = has_active_filters
        context['filter_data'] = self.process_form(request, form)
        return context

    def base_query(self):
        return AbstractFilterPage.objects.live().filter(
            CFGOVPage.objects.child_of_q(self))

    def process_form(self, request, form):
        filter_data = {}
        if form.is_valid():
            paginator = Paginator(form.get_page_set(),
                                  self.per_page_limit())
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
            paginator = Paginator([], self.per_page_limit())
            filter_data['page_set'] = paginator.page(1)
        filter_data['form'] = form
        return filter_data

    # Set up the form's data either with values from the GET request
    # or with defaults based on whether it's a dropdown/list or a text field
    def get_form_data(self, request_dict):
        form_data = {}
        has_active_filters = False
        for field in FilterableListForm.declared_fields:
            if field in ['categories', 'topics', 'authors']:
                value = request_dict.getlist(field, [])
            else:
                value = request_dict.get(field, '')
            form_data[field] = value
            if value:
                has_active_filters = True
        return form_data, has_active_filters

    def per_page_limit(self):
        return 10

    def serve(self, request, *args, **kwargs):
        """ Modify response header to set a shorter TTL in Akamai """
        response = super(FilterableListMixin, self).serve(request)
        response['Edge-Control'] = 'cache-maxage=10m'
        return response
