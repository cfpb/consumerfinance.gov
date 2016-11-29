import warnings

from bs4 import BeautifulSoup

from sheerlike.helpers import process_string_fields
from v1 import parse_links


def process_doc(doc):
    return parse_links(doc).encode(formatter=None)


def process_external_links(doc):
    warnings.filterwarnings('ignore')
    for key, value in doc.iteritems():
        doc[key] = process_string_fields(value, callback=process_doc)
    warnings.resetwarnings()
    return doc
