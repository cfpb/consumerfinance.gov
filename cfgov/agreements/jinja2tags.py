from django.db.models import Count
from django.template.loader import render_to_string

from jinja2.ext import Extension

from agreements.models import Issuer


def issuer_select(selected_issuer_slug=None):
    # Select all issuers that have associated agreements, ordered by name.
    #
    # This is equivalent to the following SQL query:
    #
    # SELECT
    #     agreements_issuer.id,
    #     agreements_issuer.name,
    #     agreements_issuer.slug,
    #     COUNT(agreements_agreement.id) AS number_of_agreements
    # FROM
    #     agreements_issuer
    # LEFT OUTER JOIN
    #     agreements_agreement
    # ON
    #     agreements_issuer.id = agreements_agreement.issuer_id
    # GROUP BY
    #     agreements_issuer.id
    # HAVING
    #     COUNT(agreements_agreement.id) > 0
    # ORDER BY
    #     agreements_issuer.name ASC
    issuers = Issuer.objects \
        .annotate(number_of_agreements=Count('agreement')) \
        .filter(number_of_agreements__gt=0) \
        .order_by('name')

    return render_to_string('agreements/_select.html', {
        'issuers': issuers,
        'selected_issuer_slug': selected_issuer_slug,
    })


class AgreementsExtension(Extension):
    """
    This will give us an {% agreements_issuer_select %} tag.
    """
    def __init__(self, environment):
        super().__init__(environment)
        self.environment.globals.update({
            'agreements_issuer_select': issuer_select,
        })


agreements = AgreementsExtension
