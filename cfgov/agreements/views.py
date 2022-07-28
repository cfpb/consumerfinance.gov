from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render

from agreements import RESULTS_PER_PAGE
from agreements.models import Agreement, Issuer


def index(request):
    return render(
        request,
        "agreements/index.html",
        {
            "agreement_count": Agreement.objects.all().count(),
            "pagetitle": "Credit card agreements",
        },
    )


def issuer_search(request, issuer_slug):
    issuers = Issuer.objects.filter(slug=issuer_slug)

    if not issuers.exists():
        raise Http404

    agreements = Agreement.objects.filter(issuer__in=issuers)

    if agreements.exists():
        issuer = agreements.latest("pk").issuer
    else:
        issuer = issuers.latest("pk")

    pager = Paginator(agreements.order_by("file_name"), RESULTS_PER_PAGE)

    try:
        page = pager.page(request.GET.get("page"))
    except PageNotAnInteger:
        page = pager.page(1)
    except EmptyPage:
        page = pager.page(pager.num_pages)

    return render(
        request,
        "agreements/search.html",
        {
            "page": page,
            "issuer": issuer,
        },
    )
