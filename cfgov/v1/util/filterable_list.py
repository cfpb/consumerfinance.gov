from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .. import forms
from ..models.learn_page import AbstractFilterPage
from ..util.util import get_secondary_nav_items

class FilterableListMixin(object):
    # Returns a queryset of AbstractFilterPages
    def get_page_set(self, form, hostname):
        return AbstractFilterPage.objects.live_shared(hostname).child_of(
            self).filter(form.generate_query()).distinct().order_by('-date_published')


    # Returns a form class to use for the filterable list
    def get_form_class(self):
        return forms.FilterableListForm


    def get_context(self, request, *args, **kwargs):
        context = {}
        try:
            context = super(FilterableListMixin, self).get_context(request, *args, **kwargs)
        except AttributeError as e:
            raise e
        context['get_secondary_nav_items'] = get_secondary_nav_items
        context['filter_data'] = self.process_forms(request, self.get_forms(request))
        return context


    def process_forms(self, request, forms):
        filter_data = {'forms': [], 'page_sets': []}
        for form in forms:
            if form.is_valid():
                paginator = Paginator(self.get_page_set(form, request.site.hostname), self.per_page_limit())
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
                filter_data['page_sets'].append([])
            filter_data['forms'].append(form)
        return filter_data


    def get_forms(self, request):
        form_class = self.specific.get_form_class()
        form_specific_filters = self.get_form_specific_filter_data(form_class, request.GET)
        return [form_class(form_data, parent=self, hostname=request.site.hostname) for form_data in form_specific_filters]


    # Transform each GET parameter key from unique ID for the form in the
    # request and assign it to a dictionary under the form ID from where it
    # came from.
    def get_form_specific_filter_data(self, form_class, request_dict):
        try:
            fields = getattr(form_class, 'declared_fields')
        except AttributeError as e:
            raise e
        filters_data = []
        for i in self.get_filter_ids():
            data = {}
            for field in fields:
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
        active_filters = False;
        form_class = self.get_form_class()
        forms_data = self.get_form_specific_filter_data(form_class, request.GET)
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
