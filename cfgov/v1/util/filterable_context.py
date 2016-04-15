from .. import forms
from .util import get_secondary_nav_items
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from ..models import base, molecules, organisms
from ref import categories as ref_categories
from ..models import CFGOVPage
from ..models.learn_page import AbstractFilterPage


def get_context(page, request, context):
    context.update({'get_secondary_nav_items': get_secondary_nav_items})
    context.update({'has_active_filters': has_active_filters})

    context['forms'] = []
    form_class = page.specific.get_form_class()
    form_specific_filters = get_form_specific_filter_data(page, form_class, request.GET)
    forms = [form_class(form_specific_filters[filters_id], parent=page, hostname=request.site.hostname)
             for filters_id in form_specific_filters.keys()]
    for form in forms:
        if form.is_valid():
            # Paginate results by 10 items per page.
            paginator = Paginator(get_page_set(page, form, request.site.hostname), 10)
            page = request.GET.get('page')

            # Get the page number in the request and get the page from the
            # paginator to serve.
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            context.update({'posts': posts})
        context['forms'].append(form)
    return context


# Transform each GET parameter key from unique ID for the form in the
# request and assign it to a dictionary under the form ID from where it
# came from.
def get_form_specific_filter_data(page, form_class, request_dict):
    filters_data = {}
    # Find every form existing on the page and assign a dictionary with its
    # number as the key.
    for i, f in enumerate(page.content):
        if 'filter_controls' in f.block_type:
            filters_data[i] = {}

    # For each form ID dictionary, find all the fields for it. Assign the
    # select fields to lists and append them for each selection. Return the
    # dictionary of normalized field names with their respective data.
    for i in filters_data.keys():
        for field in form_class.declared_fields:
            request_field_name = 'filter' + str(i) + '_' + field
            if field in ['categories', 'topics', 'authors']:
                filters_data[i][field] = \
                    request_dict.getlist(request_field_name, [])
            else:
                filters_data[i][field] = \
                    request_dict.get(request_field_name, '')
    return filters_data


# Returns a queryset of AbstractFilterPages
def get_page_set(page, form, hostname):
    from ..models.browse_filterable_page import EventArchivePage
    # If this is the Newsroom, then we need to go get the blog
    # from a different part of the site.
    blog_q = Q()
    for f in page.content:
        if 'filter_controls' in f.block_type and 'newsroom' in \
                f.value['categories']['page_type']:
            categories = form.cleaned_data.get('categories', [])
            if not categories or 'blog' in categories:
                blog_cats = [c[0] for c in ref_categories[1][1]]
                blog_q = Q(('categories__name__in', blog_cats))

    results = AbstractFilterPage.objects.live_shared(hostname).descendant_of(
        page).filter(form.generate_query())
    blogs = None
    if blog_q:
        try:
            blog = CFGOVPage.objects.get(slug='blog')
            blogs = AbstractFilterPage.objects.live_shared(hostname).descendant_of(blog)
        except CFGOVPage.DoesNotExist:
            pass

    if isinstance(page, EventArchivePage):
        filter_pages = [page.specific for page in results]
    else:
        filter_pages = [page.specific for page in results
                        if not isinstance(page.get_parent().specific, EventArchivePage)]
        if blogs:
            filter_pages += [page.specific for page in blogs]

    filter_pages.sort(key=lambda x: x.date_published, reverse=True)
    return filter_pages


def has_active_filters(page, request, index):
    active_filters = False;
    form_class = page.get_form_class()
    forms_data = get_form_specific_filter_data(page, form_class, request.GET)
    if forms_data:
        for filters in forms_data[index].values():
            for value in filters:
                if value:
                    active_filters = True

    return active_filters
