from six.moves.urllib.parse import urlparse

from django.contrib.postgres.search import SearchVector
from django.core.paginator import InvalidPage, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.six import iterlists

from prepaid_agreements.models import PrepaidProduct
from v1.models.snippets import ReusableText


def validate_page_number(request, paginator):
    """
    A utility for parsing a pagination request,
    catching invalid page numbers and always returning
    a valid page number, defaulting to 1.
    TODO: can be replaced by Paginator.get_page
    when/if upgraded to Django 2.0+
    """
    raw_page = request.GET.get('page', 1)
    try:
        page_number = int(raw_page)
    except ValueError:
        page_number = 1
    try:
        paginator.page(page_number)
    except InvalidPage:
        page_number = 1
    return page_number


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
    query = request.GET.copy()
    params = dict(iterlists(query))
    available_filters = {}
    search_term = None
    search_field = None
    products = PrepaidProduct.objects.valid()
    total_count = products.count()
    valid_filters = [
        'prepaid_type', 'status', 'issuer_name'
    ]
    if params:
        params.pop('page', None)
        search_term = params.pop('q', None)
        search_field = params.pop('search_field', None)
        if search_field:
            search_field = search_field[0]
        if search_term:
            search_term = search_term[0].strip()
            if search_term != '':
                products = search_products(
                    search_term, search_field, products
                )
            available_filters = get_available_filters(products)
        products = filter_products(params, products)

    if not available_filters:
        for filter_name in valid_filters:
            available_filters[filter_name] = PrepaidProduct.objects.order_by(
                filter_name).values_list(filter_name, flat=True).distinct()

    current_count = products.count()
    paginator = Paginator(products.all(), 20)
    page_number = validate_page_number(request, paginator)
    page = paginator.page(page_number)

    return render(request, 'prepaid_agreements/index.html', {
        'current_page': page_number,
        'results': page,
        'total_count': total_count,
        'paginator': paginator,
        'current_count': current_count,
        'filters': params,
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
    search_page_path = reverse('prepaid_agreements:index')
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
