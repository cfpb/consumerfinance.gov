from six.moves.urllib.parse import urlencode

from django.utils.six import iterlists

from jinja2.ext import Extension


def remove_url_parameter(request, discards):
    """
    Removes specified params from request query
    and returns updated querystring.
    Discards should be a dict of lists:
         {param: [values]}
    """
    query = request.GET.copy()
    params = dict(iterlists(query))
    items = {}
    for key in params:
        if key in discards:
            items[key.encode('utf-8')] = [
                item.encode('utf-8') for item in params[key]
                if item not in discards[key]]
        else:
            items[key.encode('utf-8')] = [
                item.encode('utf-8') for item in params[key]]
    querystring = urlencode(items, 'utf-8')
    return '?{}'.format(querystring) if querystring else ''


class PrepaidAgreementsExtension(Extension):
    """
    This will give us a {% remove_url_parameter %} tag.
    """
    def __init__(self, environment):
        super(PrepaidAgreementsExtension, self).__init__(environment)
        self.environment.globals.update({
            'remove_url_parameter': remove_url_parameter
        })


prepaid_agreements = PrepaidAgreementsExtension
