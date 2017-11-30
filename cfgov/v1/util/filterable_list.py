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
        filter_data = self.process_forms(request, self.get_forms(request))
        context['filter_data'] = filter_data
        return context

    def base_query(self):
        return AbstractFilterPage.objects.live().filter(
            CFGOVPage.objects.child_of_q(self))

    def process_forms(self, request, forms):
        filter_data = {'forms': [], 'page_sets': []}
        for form in forms:
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

                filter_data['page_sets'].append(pages)
            else:
                paginator = Paginator([], self.per_page_limit())
                filter_data['page_sets'].append(paginator.page(1))
            filter_data['forms'].append(form)
        return filter_data

    def get_forms(self, request):
        for form_data in self.get_form_specific_filter_data(
                request_dict=request.GET):
            yield FilterableListForm(
                form_data,
                base_query=self.base_query()
            )

    # Transform each GET parameter key from unique ID for the form in the
    # request and assign it to a dictionary under the form ID from where it
    # came from.
    def get_form_specific_filter_data(self, request_dict):
        filters_data = []
        for i in self.get_filter_ids():
            data = {}
            for field in FilterableListForm.declared_fields:
                request_field_name = 'filter' + str(i) + '_' + field
                if field in ['categories', 'topics', 'authors']:
                    data[field] = request_dict.getlist(request_field_name, [])
                else:
                    data[field] = request_dict.get(request_field_name, '')
            filters_data.append(data)
        return filters_data

    # Find every form existing on the page and assign a dictionary with its
    # number as the key.
    def get_filter_ids(self):
        keys = []
        for i, block in enumerate(self.content):
            try:
                if 'filter_controls' in block.block_type:
                    keys.append(i)
            except TypeError as e:
                raise e
        return keys

    def has_active_filters(self, request, index):
        active_filters = False
        forms_data = self.get_form_specific_filter_data(
            request_dict=request.GET)
        filter_ids = self.get_filter_ids()
        if forms_data and index in filter_ids:
            try:
                for value in forms_data[filter_ids.index(index)].values():
                    if value:
                        active_filters = True
            except TypeError as e:
                raise e

        return active_filters

    def per_page_limit(self):
        return 10

    def form_id(self):
        form_ids = self.get_filter_ids()
        if form_ids:
            return form_ids[0]
        else:
            return 0

    def serve(self, request, *args, **kwargs):
        """ Modify response header to set a shorter TTL in Akamai """
        response = super(FilterableListMixin, self).serve(request)
        response['Edge-Control'] = 'cache-maxage=10m'
        return response
