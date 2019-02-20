from jinja2 import Markup
from jinja2.ext import Extension

from agreements.models import Agreement, Issuer


def issuer_select(selected=None):
    issuers = Issuer.objects.all().order_by('name')
    issuers_filtered = []
    for issuer in issuers:
        if Agreement.objects.filter(issuer=issuer).exists():
            issuers_filtered.append(issuer)

    markup = '<select data-placeholder="Choose an issuer"'
    markup += ' class="chzn-select" tabindex="2" id="issuer_select">'

    for i in issuers_filtered:
        markup += '<option value="' + i.slug + '"'
        if selected == i.slug:
            markup += ' selected'
        markup += '>' + i.name + '</option>'
    markup += '</select>'
    return Markup(markup)


class AgreementsExtension(Extension):
    """
    This will give us a {% issuer_select %} tag.
    """
    def __init__(self, environment):
        super(AgreementsExtension, self).__init__(environment)
        self.environment.globals.update({
            'issuer_select': issuer_select,
        })


agreements = AgreementsExtension
