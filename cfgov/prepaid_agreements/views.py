from urllib.parse import urlparse

from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse

from prepaid_agreements.forms import FilterForm, SearchForm
from prepaid_agreements.models import PrepaidProduct
from v1.models.snippets import ReusableText


def get_available_filters(products):
    available_filters = {'prepaid_type': [], 'status': [], 'issuer_name': []}

    for product in products.all():
        prepaid_type = product.prepaid_type
        if prepaid_type and prepaid_type != '':
            if prepaid_type not in available_filters['prepaid_type']:
                available_filters['prepaid_type'].append(prepaid_type)

        status = product.status
        if status and status not in available_filters['status']:
            available_filters['status'].append(status)

        issuer_name = product.issuer_name
        if issuer_name and issuer_name not in available_filters['issuer_name']:
            available_filters['issuer_name'].append(issuer_name)

    return available_filters


def search_products(search_term, search_field, products):
    search_fields = [
        'issuer_name',
        'other_relevant_parties',
        'name',
        'program_manager',
        'prepaid_type',
    ]
    if search_field and search_field in search_fields:
        search_fields = [search_field]
    products = products.annotate(
        search=SearchVector(
            *search_fields
        ),
    ).filter(search=search_term)

    return products


def filter_products(filters, products):
    if 'issuer_name' in filters:
        issuers = Q()
        for issuer in filters['issuer_name']:
            issuers |= Q(issuer_name__iexact=issuer)
        products = products.filter(issuers)

    if 'prepaid_type' in filters:
        prepaid_types = Q()
        for prepaid_type in filters['prepaid_type']:
            prepaid_types |= Q(prepaid_type__iexact=prepaid_type)
        products = products.filter(prepaid_types)

    if 'status' in filters:
        products = products.filter(status__iexact=filters['status'][0])

    return products


def get_disclaimer_text():
    return ReusableText.objects.filter(
        title='Prepaid agreements database disclaimer').first()


def get_support_text():
    return ReusableText.objects.filter(
        title='Prepaid agreements support and inquiries').first()


def index(request):
    products = PrepaidProduct.objects.valid()
    total_count = products.count()
    valid_filters = [
        'prepaid_type', 'status', 'issuer_name'
    ]
    available_filters = {}

    # Provide valid initial values for the search form so that it is always
    # valid. A blank search will return all products.
    page_number = 1
    search_term = ''
    search_field = 'all'
    search_form = SearchForm(
        request.GET,
        initial={
            'q': search_term,
            'search_field': search_field,
            'page': page_number,
        }
    )
    # Get our search results. If the form is not valid, our default search_term
    # and search_field will be used below.
    if search_form.is_valid():
        page_number = search_form.cleaned_data['page']
        search_field = search_form.cleaned_data['search_field']
        search_term = search_form.cleaned_data['q'].strip()
        if search_term != '':
            products = search_products(
                search_term, search_field, products
            )

    # Get the available filters for products in the search results and then set
    # those filter choices on the filter form
    filters = {}
    available_filters = get_available_filters(products)
    filter_form = FilterForm(request.GET)
    filter_form.set_issuer_name_choices(available_filters['issuer_name'])
    filter_form.set_prepaid_type_choices(available_filters['prepaid_type'])
    filter_form.set_status_choices(available_filters['status'])

    # Filter our products based on the sanitized values from the filter form.
    # If the form is not valid, the products already selected based on the
    # search form will be used below.
    if filter_form.is_valid():
        filters = {
            k: filter_form.cleaned_data[k]
            for k in valid_filters
            if filter_form.cleaned_data[k]
        }
        products = filter_products(filters, products)

    current_count = products.count()

    # Handle pagination
    paginator = Paginator(products.all(), 25)
    page = paginator.get_page(page_number)

    return TemplateResponse(request, 'prepaid_agreements/index.html', {
        'current_page': page.number,
        'results': page,
        'total_count': total_count,
        'paginator': paginator,
        'current_count': current_count,
        'filters': filters,
        'query': search_term or '',
        'active_filters': available_filters,
        'valid_filters': valid_filters,
        'search_field': search_field,
        'disclaimer_text': get_disclaimer_text(),
        'support_text': get_support_text()
    })


def get_detail_page_breadcrumb(request):
    """
    Determines link back to search page from detail page.
    If referrer is search page and contains a query
    string, returns referrer so query is preserved.
    Otherwise, returns base search page path.
    """
    http_referer = request.META.get('HTTP_REFERER', '')
    referrer = urlparse(http_referer)
    search_page_path = reverse("prepaid_agreements:index")
    if referrer.query and referrer.path == search_page_path:
        return http_referer
    else:
        return search_page_path


def detail(request, product_id):
    return render(request, 'prepaid_agreements/detail.html', {
        'product': get_object_or_404(PrepaidProduct, pk=product_id),
        'search_page_url': get_detail_page_breadcrumb(request),
        'disclaimer_text': get_disclaimer_text(),
        'support_text': get_support_text()
    })
