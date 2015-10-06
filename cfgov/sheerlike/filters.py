import re
import calendar
import datetime
from dateutil.parser import parse

from .middleware import get_request

def generate_term_filters(multidict, filter_keys):
    '''
    This generates the ElasticSearch filter DSL for filters that check whether
    a field matches a certain string.  Groupings of the same exact filter, such
    as filter_fieldname, are combined into an OR filter, while the major
    groupings of separate filters are all combined into an AND filter.
    '''
    term_main = {"and": []}
    for key in filter_keys:
        field = key.replace('filter_', '')
        filter_type_main = {"or": []}
        values = multidict.getlist(key)
        #from nose.tools import set_trace; set_trace();
        for val in values:
            term_single = {"term": {}}
            term_single["term"][field] = val
            filter_type_main["or"].append(term_single)
        term_main["and"].append(filter_type_main)
    return term_main

def generate_range_filters(multidict, filter_keys):
    '''
    This generates the ElasticSearch filter DSL for filters that check whether
    a field is within a certain range
    '''
    range_clause = {"range": {}}
    for key in filter_keys:
        full_field = key.replace('filter_range_', '')
        # We account for potential underscores in the field name itself
        # e.g. comment_count
        operator = full_field[full_field.rfind('_') + 1:]
        field = full_field[:full_field.rfind('_')]
        if field not in range_clause["range"]:
            range_clause["range"][field] = {}
        # If there are multiples of the same date filter, this will take
        # the first
        
        # The django version of MultiDict returns the actual object
        # if there is only one, and a list otherwise
        value = multidict.get(key)
        range_clause["range"][field][operator] = value

    # Validate date range input

    # First check if both date_lte and date_gte are present
    # If the 'start' date is after the 'end' date, swap them
    if 'date' in range_clause['range']:
        if all(x in range_clause['range']['date'] for x in ('lte', 'gte')) and \
            parse(range_clause['range']['date']['gte'], default=datetime.date.today().replace(day=1)) > \
                parse(range_clause['range']['date']['lte'], default=datetime.date.today().replace(day=1)):
            range_clause['range']['date']['gte'], range_clause['range']['date']['lte'] = \
                range_clause['range']['date'][
                    'lte'], range_clause['range']['date']['gte']
        # If either date matches the YYYY-M[M] format, append the
        # appropriate day
        if 'lte' in range_clause['range']['date'] and \
                re.compile("^[0-9]{4}-[0-9]{1,2}$").match(range_clause['range']['date']['lte']):
            year, month = range_clause['range']['date']['lte'].split('-')
            last_day_of_month = calendar.monthrange(
                int(year), int(month))[1]
            range_clause['range']['date'][
                'lte'] += "-{0}".format(last_day_of_month)
        if 'gte' in range_clause['range']['date'] and \
                re.compile("^[0-9]{4}-[0-9]{1,2}$").match(range_clause['range']['date']['gte']):
            range_clause['range']['date']['gte'] += "-1"
    return range_clause



def filter_dsl_from_multidict(multidict):
    # Split the filters between 'range' and 'term', making sure the query
    # value isn't blank
    term_filter_keys = [r for r in [k for k in multidict.keys() if re.compile("^filter_(?!range_)").match(k)]
                        if multidict[r]]
    range_filter_keys = [r for r in [k for k in multidict.keys() if re.compile("^filter_range_").match(k)]
                         if multidict[r]]
    final_filters = []
    if term_filter_keys:
        term_clause = generate_term_filters(multidict, term_filter_keys)
        final_filters.append(term_clause)
        
    if range_filter_keys:
        range_clause = generate_range_filters(multidict, range_filter_keys)
        final_filters.append(range_clause)
    return final_filters


def selected_filters_from_multidict(multidict, field):
    return [k for k in multidict.getlist('filter_' + field) if k]


def selected_filters_for_field(fieldname):
    multidict = get_request().GET
    return selected_filters_from_multidict(multidict, fieldname)


def is_filter_selected(fieldname, value):
    multidict = get_request().GET
    return value in selected_filters_from_multidict(multidict, fieldname)

