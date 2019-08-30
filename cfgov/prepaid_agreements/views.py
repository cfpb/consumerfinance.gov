from django.contrib.postgres.search import SearchVector
from django.core.paginator import InvalidPage, Paginator
from django.db.models import Q
from django.shortcuts import render

from prepaid_agreements.models import PrepaidProduct


def validate_page_number(request, paginator):
    """
    A utility for parsing a pagination request,
    catching invalid page numbers and always returning
    a valid page number, defaulting to 1.
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


def search_products(search_term, search_field, products):
    search_fields = [
        'issuer_name',
        'other_relevant_parties',
        'name',
        'program_manager',
        'prepaid_type',
    ]
    if search_field and search_field[0] in search_fields:
        search_fields = [search_field[0]]
    products = products.annotate(
        search=SearchVector(
            *search_fields
        ),
    ).filter(search=search_term)
    active_filters = {'prepaid_type': [], 'status': [], 'issuer_name': []}
    for product in products:
        if product.prepaid_type not in active_filters['prepaid_type']:
            if product.prepaid_type != '':
                active_filters['prepaid_type'].append(
                    product.prepaid_type)
        if product.status not in active_filters['status']:
            active_filters['status'].append(product.status)
        if product.issuer_name not in active_filters['issuer_name']:
            active_filters['issuer_name'].append(product.issuer_name)
    return products, active_filters


def index(request):
    filters = dict(request.GET.iterlists())
    active_filters = {}
    search_term = None
    search_field = None
    products = PrepaidProduct.objects
    total_count = products.count()
    valid_filters = [
        'prepaid_type', 'status', 'issuer_name'
    ]
    active_filters_populated = False
    if filters:
        filters.pop('page', None)
        search_term = filters.pop('q', None)
        search_field = filters.pop('search_field', None)

        if search_term:
            search_term = search_term[0].strip()
            if search_term != '':
                products, active_filters = search_products(
                    search_term, search_field, products
                )
            active_filters_populated = True

        if 'issuer_name' in filters:
            issuers = Q()
            for issuer in filters['issuer_name']:
                issuers |= Q(issuer_name__iexact=issuer)
            products = products.filter(issuers)

        if 'prepaid_type' in filters:
            prepaid_types = Q()
            for prepaid_type in filters['prepaid_type']:
                prepaid_types |= Q(prepaid_type__iexact=prepaid_type.title())
            products = products.filter(prepaid_types)

        if 'status' in filters:
            products = products.filter(status__iexact=filters['status'][0])

    current_count = products.count()
    paginator = Paginator(products.all(), 20)
    page_number = validate_page_number(request, paginator)
    page = paginator.page(page_number)

    if not active_filters_populated:
        for filter_name in valid_filters:
            active_filters[filter_name] = PrepaidProduct.objects.order_by(
                filter_name).values_list(filter_name, flat=True).distinct()

    return render(request, 'prepaid_agreements/index.html', {
        'current_page': page_number,
        'results': page,
        'total_count': total_count,
        'paginator': paginator,
        'current_count': current_count,
        'filters': filters,
        'query': search_term or '',
        'active_filters': active_filters,
        'valid_filters': valid_filters,
        'search_field': search_field,
    })


def detail(request, product_id):
    return render(request, 'prepaid_agreements/detail.html', {
        'product': PrepaidProduct.objects.get(id=product_id)
    })
