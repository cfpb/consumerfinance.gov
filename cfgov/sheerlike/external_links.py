import warnings
from v1 import parse_links


def process_external_links(doc):
    warnings.filterwarnings('ignore')
    for key, value in doc.iteritems():
        doc[key] = _process_data(value)
    warnings.resetwarnings()
    return doc


def _process_data(field):
    if isinstance(field, basestring):
        field = parse_links(field).encode(formatter=None)
    elif isinstance(field, list):
        for i, value in enumerate(field):
            field[i] = _process_data(value)
    elif isinstance(field, dict):
        for key, value in field.iteritems():
            field[key] = _process_data(value)
    return field
