import collections
import re
from time import time
from django.conf import settings
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.blocks.struct_block import StructValue



def id_validator(id_string, search=re.compile(r'[^a-zA-Z0-9-_]').search):
    if id_string:
        return not bool(search(id_string))
    else:
        return False


# example_case ==> ExampleCase
def to_camel_case(snake_str):
    snake_str = snake_str.capitalize()
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def get_unique_id(prefix='', suffix=''):
    index = hex(int(time()*10000000))[2:]
    return prefix + str(index) + suffix


 # These messages are manually mirrored on the
 # Javascript side in error-messages-config.js
ERROR_MESSAGES = {
    'CHECKBOX_ERRORS' : {
        'required' : 'Please select at least one of the "%s" options.'
    },
    'DATE_ERRORS' :{
        'invalid' : 'You have entered an invalid date.',
        'one_required': 'Please enter at least one date.'
    }
}


# Orders by most to least common in the given list.
def most_common(lst):
    # Returns the lst if empty or there's just one element in it.
    if not lst or len(lst) == 1:
        return lst
    else:
        # Gets the most common element in the list.
        most = max(set(lst), key=lst.count)
        # Creates a new list without that element.
        new_list = [e for e in lst if most not in e]
        # Recursively returns a list with the most common elements ordered
        # most to least. Ties go to the lowest index in the given list.
        return [most] + most_common(new_list)


def get_form_id(page, get_request):
        form_ids = []
        if callable(getattr(page, 'get_form_specific_filter_data', None)):
            form_ids = page.get_form_specific_filter_data(page.get_form_class(),
                                                          get_request).keys()
        if form_ids:
            return form_ids[0]
        else:
            return None
