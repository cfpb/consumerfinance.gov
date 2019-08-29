from six import iteritems
from six.moves.urllib.parse import urlencode

from jinja2.ext import Extension


def remove_url_parameter(request, params_to_remove):
    """
    Removes specified params from request query
    and returns updated querystring.
    Params for removal should be in format:
         {param_name: [values]}
    """
    query = request.GET.copy()
    current_params = dict(query.iterlists())
    for key in params_to_remove:
        if key in current_params:
            for val in params_to_remove[key]:
                if val in current_params[key]:
                    current_params[key].remove(val)
    querystring = urlencode(current_params, 'utf-8')
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
