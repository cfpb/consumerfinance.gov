from django import template
from django.template.loader import render_to_string

from agreements.models import Agreement, Issuer


register = template.Library()


@register.simple_tag
def issuer_select(selected=None):
    issuers = Issuer.objects.all().order_by('name')
    issuers_filtered = []
    for issuer in issuers:
        if Agreement.objects.filter(issuer=issuer).exists():
            issuers_filtered.append(issuer)

    return render_to_string('agreements/issuer_select.html', {
        'issuers': issuers_filtered,
        'selected': selected
    })
