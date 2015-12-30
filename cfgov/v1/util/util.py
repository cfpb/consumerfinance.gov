import re
from django.conf import settings


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
