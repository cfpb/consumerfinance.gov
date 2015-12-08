import re


def id_validator(id_string, search=re.compile(r'[^a-zA-Z0-9-_]').search):
    if id_string:
        return not bool(search(id_string))
    else:
        return False
